"""
tests.test_shell_command
~~~~~~~~~~~~~~~~~~~~~~~~

Tests demo component.
"""
import os
import tempfile
import unittest
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from homeassistant import core
from homeassistant.components import shell_command
from homeassistant.util.compat import TemporaryDirectory


class TestShellCommand(unittest.TestCase):
    """ Test the demo module. """

    def setUp(self):  # pylint: disable=invalid-name
        self.hass = core.HomeAssistant()

    def tearDown(self):  # pylint: disable=invalid-name
        """ Stop down stuff we started. """
        self.hass.stop()

    def test_executing_service(self):
        """ Test if able to call a configured service. """
        with TemporaryDirectory() as tempdirname:
            path = os.path.join(tempdirname, 'called.txt')
            self.assertTrue(shell_command.setup(self.hass, {
                'shell_command': {
                    'test_service': "date > {}".format(path)
                }
            }))

            self.hass.services.call('shell_command', 'test_service',
                                    blocking=True)

            self.assertTrue(os.path.isfile(path))

    def test_config_not_dict(self):
        """ Test if config is not a dict. """
        self.assertFalse(shell_command.setup(self.hass, {
            'shell_command': ['some', 'weird', 'list']
            }))

    def test_config_not_valid_service_names(self):
        """ Test if config contains invalid service names. """
        self.assertFalse(shell_command.setup(self.hass, {
            'shell_command': {
                'this is invalid because space': 'touch bla.txt'
            }}))

    @patch('homeassistant.components.shell_command.subprocess.call',
           side_effect=Exception)
    @patch('homeassistant.components.shell_command._LOGGER.error')
    def test_subprocess_raising_error(self, mock_call, mock_error):
        with TemporaryDirectory() as tempdirname:
            path = os.path.join(tempdirname, 'called.txt')
            self.assertTrue(shell_command.setup(self.hass, {
                'shell_command': {
                    'test_service': "touch {}".format(path)
                }
            }))

            self.hass.services.call('shell_command', 'test_service',
                                    blocking=True)

            self.assertFalse(os.path.isfile(path))
            self.assertEqual(1, mock_error.call_count)
