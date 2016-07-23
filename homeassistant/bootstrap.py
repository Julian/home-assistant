"""Provides methods to bootstrap a home assistant instance."""

from collections import defaultdict
import errno
import logging
import logging.handlers
import os
import sys
from collections import defaultdict
from threading import RLock

import voluptuous as vol

import homeassistant.components as core_components
from homeassistant.components import group, persistent_notification
import homeassistant.config as conf_util
import homeassistant.core as core
import homeassistant.helpers.config_validation as cv
import homeassistant.loader as loader
from homeassistant.const import EVENT_COMPONENT_LOADED, PLATFORM_FORMAT
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import (
    event_decorators, service, config_per_platform, extract_domain_configs)

_LOGGER = logging.getLogger(__name__)
_SETUP_LOCK = RLock()
_CURRENT_SETUP = []

ATTR_COMPONENT = 'component'

ERROR_LOG_FILENAME = 'home-assistant.log'


def setup_component(hass, domain, config=None):
    """Setup a component and all its dependencies."""
    if domain in hass.config.components:
        return True

    _ensure_loader_prepared(hass)

    if config is None:
        config = defaultdict(dict)

    components = loader.load_order_component(domain)

    # OrderedSet is empty if component or dependencies could not be resolved
    if not components:
        return False

    for component in components:
        if not _setup_component(hass, component, config):
            return False

    return True


def _setup_component(hass, domain, config):
    """Setup a component for Home Assistant."""
    # pylint: disable=too-many-return-statements,too-many-branches
    if domain in hass.config.components:
        return True

    with _SETUP_LOCK:
        # It might have been loaded while waiting for lock
        if domain in hass.config.components:
            return True

        if domain in _CURRENT_SETUP:
            _LOGGER.error('Attempt made to setup %s during setup of %s',
                          domain, domain)
            return False

        component = loader.get_component(domain)
        _CURRENT_SETUP.append(domain)
        try:
            if not component.setup(hass, config):
                _LOGGER.error('component %s failed to initialize', domain)
                return False
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception('Error during setup of component %s', domain)
            return False

        try:
            if not component.setup(hass, config):
                _LOGGER.error('component %s failed to initialize', domain)
                return False
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception('Error during setup of component %s', domain)
            return False
        finally:
            _CURRENT_SETUP.remove(domain)

        hass.config.components.append(component.DOMAIN)

        # Assumption: if a component does not depend on groups
        # it communicates with devices
        if group.DOMAIN not in getattr(component, 'DEPENDENCIES', []):
            hass.pool.add_worker()

        hass.bus.fire(
            EVENT_COMPONENT_LOADED, {ATTR_COMPONENT: component.DOMAIN})

        return True


def prepare_setup_platform(hass, config, domain, platform_name):
    """Load a platform and makes sure dependencies are setup."""
    _ensure_loader_prepared(hass)

    platform_path = PLATFORM_FORMAT.format(domain, platform_name)

    platform = loader.get_platform(domain, platform_name)

    # Not found
    if platform is None:
        _LOGGER.error('Unable to find platform %s', platform_path)
        return None

    # Already loaded
    elif platform_path in hass.config.components:
        return platform

    # Load dependencies
    for component in getattr(platform, 'DEPENDENCIES', []):
        if not setup_component(hass, component, config):
            _LOGGER.error(
                'Unable to prepare setup for platform %s because '
                'dependency %s could not be initialized', platform_path,
                component)
            return None

    return platform


# pylint: disable=too-many-branches, too-many-statements, too-many-arguments
def from_config_dict(config, hass=None, config_dir=None, enable_log=True,
                     verbose=False):
    """
    Tries to configure Home Assistant from a config dict.

    Dynamically loads required components and its dependencies.
    """
    if hass is None:
        hass = core.HomeAssistant()
        if config_dir is not None:
            config_dir = os.path.abspath(config_dir)
            hass.config.config_dir = config_dir
            _mount_local_lib_path(config_dir)

    core_config = config.get(core.DOMAIN, {})

    try:
        conf_util.process_ha_core_config(hass, core_config)
    except vol.Invalid as ex:
        cv.log_exception(_LOGGER, ex, 'homeassistant', core_config)
        return None

    conf_util.process_ha_config_upgrade(hass)

    if enable_log:
        enable_logging(hass, verbose)

    _ensure_loader_prepared(hass)

    # Make a copy because we are mutating it.
    # Convert it to defaultdict so components can always have config dict
    # Convert values to dictionaries if they are None
    config = defaultdict(
        dict, {key: value or {} for key, value in config.items()})

    # Filter out the repeating and common config section [homeassistant]
    components = set(key.split(' ')[0] for key in config.keys()
                     if key != core.DOMAIN)

    if not core_components.setup(hass, config):
        _LOGGER.error('Home Assistant core failed to initialize. '
                      'Further initialization aborted.')
        return hass

    persistent_notification.setup(hass, config)

    _LOGGER.info('Home Assistant core initialized')

    # Give event decorators access to HASS
    event_decorators.HASS = hass
    service.HASS = hass

    # Setup the components
    for domain in loader.load_order_components(components):
        _setup_component(hass, domain, config)

    return hass


def from_config_file(config_path, hass=None, verbose=False):
    """
    Reads the configuration file and tries to start all the required
    functionality. Will add functionality to 'hass' parameter if given,
    instantiates a new Home Assistant object if 'hass' is not given.
    """
    if hass is None:
        hass = core.HomeAssistant()

    # Set config dir to directory holding config file
    config_dir = os.path.abspath(os.path.dirname(config_path))
    hass.config.config_dir = config_dir
    _mount_local_lib_path(config_dir)

    enable_logging(hass, verbose)

    try:
        config_dict = conf_util.load_yaml_config_file(config_path)
    except HomeAssistantError:
        return None

    return from_config_dict(config_dict, hass, enable_log=False)


def enable_logging(hass, verbose=False):
    """ Setup the logging for home assistant. """
    logging.basicConfig(level=logging.INFO)
    fmt = ("%(log_color)s%(asctime)s %(levelname)s (%(threadName)s) "
            "[%(name)s] %(message)s%(reset)s")
    try:
        from colorlog import ColoredFormatter
        logging.getLogger().handlers[0].setFormatter(ColoredFormatter(
            fmt,
            datefmt='%y-%m-%d %H:%M:%S',
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red',
            }
        ))
    except ImportError:
        _LOGGER.warning(
            "Colorlog package not found, console coloring disabled")

        err_handler = logging.StreamHandler()
        err_handler.setLevel(logging.INFO if verbose else logging.WARNING)
        err_handler.setFormatter(
            logging.Formatter('%(asctime)s %(name)s: %(message)s',
                              datefmt='%y-%m-%d %H:%M:%S'))
        logger = logging.getLogger('')
        logger.addHandler(err_handler)
        logger.setLevel(logging.INFO)


def _ensure_loader_prepared(hass):
    """Ensure Home Assistant loader is prepared."""
    if not loader.PREPARED:
        loader.prepare(hass)


def _mount_local_lib_path(config_dir):
    """Add local library to Python Path."""
    sys.path.insert(0, os.path.join(config_dir, 'deps'))
