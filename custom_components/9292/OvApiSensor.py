import constants
import json

from homeassistant.const import (CONF_NAME, STATE_UNKNOWN)
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)


class OvApiSensor(Entity):
    def __init__(self, ov_api, name, destination, counter):
        self._json_data = ov_api
        self._name = name
        self._destination = destination
        self._sensor_number = counter
        self._station_name = None
        self._transport_type = None
        self._departure = None
        self._delay = None
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def station_name(self):
        return self._station_name

    @property
    def transport_type(self):
        return self._transport_type

    @property
    def departure(self):
        return self._departure

    @property
    def delay(self):
        return self._delay

    @property
    def state(self):
        return self._state

    @property
    def device_state_attributes(self):
        return {
            constants.ATTR_NAME: self._name,
            constants.ATTR_DESTINATION: self._destination,
            constants.ATTR_SENSOR_NUMBER: self._sensor_number,
            constants.ATTR_TRANSPORT_TYPE: self._transport_type,
            constants.ATTR_STOP_NAME: self._stop_name,
            constants.ATTR_DEPARTURE: self._departure,
            constants.ATTR_DELAY: self._delay,
            constants.ATTR_UPDATE_CYCLE: str(constants.MIN_TIME_BETWEEN_UPDATES.seconds) + ' seconds',
            constants.ATTR_CREDITS: constants.CONF_CREDITS
        }

    def update(self):
        """Get the latest data from the 9292OV Api."""
        self._json_data.update()

        data = json.loads(self._json_data.result)

        if data is None:
            self._departure = STATE_UNKNOWN
            self._delay = STATE_UNKNOWN
            self._state = STATE_UNKNOWN
        else:
            departures = [departure for departure in data.tabs[0].departures if
                          departure.destinationName == constants.CONF_DESTINATION]
            if departures[self._sensor_number] is None:
                self._departure = STATE_UNKNOWN
                self._delay = STATE_UNKNOWN
                self._state = STATE_UNKNOWN
            else:
                item = departures[self._sensor_number]
                self._station_name = data.tabs[0].locations[0].name
                self._transport_type = data.tabs[0].name
                self._departure = departures.time
                self._delay = departures.realtimeText
                self._state = departures.time