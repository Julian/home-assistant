"""
tests.test_component_demo
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tests demo component.
"""
import json
import unittest
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

import homeassistant.core as ha
import homeassistant.components.demo as demo
from homeassistant.remote import JSONEncoder

from tests.common import mock_http_component


@patch('homeassistant.components.sun.setup')
class TestDemo(unittest.TestCase):
    """ Test the demo module. """

    def setUp(self):  # pylint: disable=invalid-name
        self.hass = ha.HomeAssistant()
        mock_http_component(self.hass)

    def tearDown(self):  # pylint: disable=invalid-name
        """ Stop down stuff we started. """
        self.hass.stop()

    def test_if_demo_state_shows_by_default(self, mock_sun_setup):
        """ Test if demo state shows if we give no configuration. """
        demo.setup(self.hass, {demo.DOMAIN: {}})

        self.assertIsNotNone(self.hass.states.get('a.Demo_Mode'))

    def test_hiding_demo_state(self, mock_sun_setup):
        """ Test if you can hide the demo card. """
        demo.setup(self.hass, {demo.DOMAIN: {'hide_demo_state': 1}})

        self.assertIsNone(self.hass.states.get('a.Demo_Mode'))

    def test_all_entities_can_be_loaded_over_json(self, mock_sun_setup):
        """ Test if you can hide the demo card. """
        demo.setup(self.hass, {demo.DOMAIN: {'hide_demo_state': 1}})

        try:
            json.dumps(self.hass.states.all(), cls=JSONEncoder)
        except Exception:
            self.fail('Unable to convert all demo entities to JSON. '
                      'Wrong data in state machine!')
