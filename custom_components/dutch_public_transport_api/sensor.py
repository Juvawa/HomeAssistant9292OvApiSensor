import json
from datetime import timedelta
import logging
import http.client

import voluptuous as vol

import homeassistant.helpers.config_validation as cv

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME, STATE_UNKNOWN
from homeassistant.exceptions import PlatformNotReady
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

__version__ = "0.1"
_LOGGER = logging.getLogger(__name__)
_RESOURCE = "api.9292.nl"

CONF_NAME = "name"
CONF_LOCATION = "location"
CONF_DESTINATION = "destination"
CONF_SHOW_FUTURE_DEPARTURES = "show_future_departures"
CONF_DATE_FORMAT = "date_format"
CONF_CREDITS = "Data provided by api.9292.nl"

DEFAULT_NAME = "9292OV"
DEFAULT_DATE_FORMAT = "%y-%m-%dT%H:%M:%S"
DEFAULT_SHOW_FUTURE_DEPARTURES = 0

ATTR_STOP_NAME = "stop_name"
ATTR_LOCATION = "location"
ATTR_DESTINATION = "destination"
ATTR_TRANSPORT_TYPE = "transport_type"
ATTR_DEPARTURE = "departure"
ATTR_DELAY = "delay"
ATTR_UPDATE_CYCLE = "update_cycle"
ATTR_CREDITS = "credits"
ATTR_NAME = "name"

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=60)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Required(CONF_LOCATION, default=CONF_LOCATION): cv.string,
        vol.Required(CONF_DESTINATION, default=CONF_DESTINATION): cv.string,
        vol.Optional(
            CONF_SHOW_FUTURE_DEPARTURES, default=DEFAULT_SHOW_FUTURE_DEPARTURES
        ): cv.positive_int,
        vol.Optional(CONF_DATE_FORMAT, default=DEFAULT_DATE_FORMAT): cv.string,
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    name = config.get(CONF_NAME)
    location = config.get(CONF_LOCATION)
    destination = config.get(CONF_DESTINATION)
    future_departures = config.get(CONF_SHOW_FUTURE_DEPARTURES)

    ov_api = OvApiData(location)

    ov_api.update()

    if ov_api is None:
        raise PlatformNotReady

    sensors = []

    for counter in range(future_departures + 1):
        if counter == 0:
            sensors.append(OvApiSensor(ov_api, name, destination, counter))
        else:
            sensors.append(
                OvApiSensor(
                    ov_api, name + "_future_" + str(counter), destination, counter
                )
            )

    add_entities(sensors, True)


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
            ATTR_NAME: self._name,
            ATTR_DESTINATION: self._destination,
            ATTR_TRANSPORT_TYPE: self._transport_type,
            ATTR_DEPARTURE: self._departure,
            ATTR_DELAY: self._delay,
            ATTR_UPDATE_CYCLE: str(MIN_TIME_BETWEEN_UPDATES.seconds) + " seconds",
            ATTR_CREDITS: CONF_CREDITS,
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
            departures = [
                departure
                for departure in data['tabs'][0]['departures']
                if departure['destinationName'] == self._destination
            ]
            if self._sensor_number >= len(departures):
                self._departure = STATE_UNKNOWN
                self._delay = STATE_UNKNOWN
                self._state = STATE_UNKNOWN
            else:
                item = departures[self._sensor_number]
                self._station_name = data['tabs'][0]['locations'][0]['name']
                self._transport_type = data['tabs'][0]['name']
                self._departure = item['time']
                self._delay = item['realtimeText']
                self._state = item['time']


class OvApiData:
    def __init__(self, location):
        self._resource = _RESOURCE
        self._location = location
        self.result = ""
        self._headers = {"cache-control": "no-cache", "accept": "application/json"}

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        if self._location == CONF_LOCATION:
            _LOGGER.error("Impossible to get data from 9292OV Api, no location.")
            self.result = "Impossible to get data from 9292OV Api, no location."
        else:
            try:
                response = http.client.HTTPConnection(self._resource, timeout=1)
                response.request(
                    "GET",
                    "/0.1/locations/" + self._location + "/departure-times?lang=nl-NL",
                    headers=self._headers,
                )
                result = response.getresponse()
                self.result = result.read().decode("utf-8")
            except http.client.HTTPException:
                _LOGGER.error("Impossible to get data from 929OV Api using location.")
                self.result = "Impossible to get data from 929OV Api using location."
