""" Starts home assistant. """
from __future__ import print_function

from io import open
from multiprocessing import Process
import signal
import sys
import threading
import os
import argparse
import time

from homeassistant import bootstrap
import homeassistant.config as config_util
from homeassistant.const import (__version__, EVENT_HOMEASSISTANT_START,
                                 RESTART_EXIT_CODE)


def ensure_config_path(config_dir):
    """ Validates configuration directory. """

    lib_dir = os.path.join(config_dir, 'lib')

    # Test if configuration directory exists
    if not os.path.isdir(config_dir):
        if config_dir != config_util.get_default_config_dir():
            print(('Fatal Error: Specified configuration directory does '
                   'not exist {} ').format(config_dir))
            sys.exit(1)

        try:
            os.mkdir(config_dir)
        except OSError:
            print(('Fatal Error: Unable to create default configuration '
                   'directory {} ').format(config_dir))
            sys.exit(1)

    # Test if library directory exists
    if not os.path.isdir(lib_dir):
        try:
            os.mkdir(lib_dir)
        except OSError:
            print(('Fatal Error: Unable to create library '
                   'directory {} ').format(lib_dir))
            sys.exit(1)


def ensure_config_file(config_dir):
    """ Ensure configuration file exists. """
    config_path = config_util.ensure_config_exists(config_dir)

    if config_path is None:
        print('Error getting configuration path')
        sys.exit(1)

    return config_path


def get_arguments():
    """ Get parsed passed in arguments. """
    parser = argparse.ArgumentParser(
        description="Home Assistant: Observe, Control, Automate.")
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument(
        '-c', '--config',
        metavar='path_to_config_dir',
        default=config_util.get_default_config_dir(),
        help="Directory that contains the Home Assistant configuration")
    parser.add_argument(
        '--demo-mode',
        action='store_true',
        help='Start Home Assistant in demo mode')
    parser.add_argument(
        '--open-ui',
        action='store_true',
        help='Open the webinterface in a browser')
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help="Enable verbose logging to file.")

    return parser.parse_args()


def setup_and_run_hass(config_dir, args):
    """
    Setup HASS and run. Block until stopped."""
    if args.demo_mode:
        config = {
            'frontend': {},
            'demo': {}
        }
        hass = bootstrap.from_config_dict(
            config, config_dir=config_dir, verbose=args.verbose)
    else:
        config_file = ensure_config_file(config_dir)
        print('Config directory:', config_dir)
        hass = bootstrap.from_config_file(config_file, verbose=args.verbose)

    if args.open_ui:
        def open_browser(event):
            """ Open the webinterface in a browser. """
            if hass.config.api is not None:
                import webbrowser
                webbrowser.open(hass.config.api.base_url)

        hass.bus.listen_once(EVENT_HOMEASSISTANT_START, open_browser)

    hass.start()
    exit_code = int(hass.block_till_stopped())

    return exit_code


def main():
    """ Starts Home Assistant. """
    args = get_arguments()

    config_dir = os.path.join(os.getcwd(), args.config)
    ensure_config_path(config_dir)

    exit_code = setup_and_run_hass(config_dir, args)
    if exit_code == RESTART_EXIT_CODE:
        sys.stderr.write('Home Assistant requested a restart\n')
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
