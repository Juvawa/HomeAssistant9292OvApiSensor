from datetime import timedelta
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv


CONF_NAME = 'name'
CONF_LOCATION = 'location'
CONF_DESTINATION = 'destination'
CONF_SHOW_FUTURE_DEPARTURES = 'show_future_departures'
CONF_DATE_FORMAT = 'date_format'
CONF_CREDITS = 'Data provided by api.9292.nl'

DEFAULT_NAME = '9292OV'
DEFAULT_DATE_FORMAT = "%y-%m-%dT%H:%M:%S"
DEFAULT_SHOW_FUTURE_DEPARTURES = 0

ATTR_LOCATION = 'location'
ATTR_DESTINATION = 'destination'
ATTR_TRANSPORT_TYPE = 'transport_type'
ATTR_DEPARTURE = 'departure'
ATTR_DELAY = 'delay'
ATTR_UPDATE_CYCLE = 'update_cycle'
ATTR_CREDITS = 'credits'

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=60)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_LOCATION, default=CONF_LOCATION): cv.string,
    vol.Required(CONF_DESTINATION, default=CONF_DESTINATION): cv.string,
    vol.Optional(CONF_SHOW_FUTURE_DEPARTURES, default=DEFAULT_SHOW_FUTURE_DEPARTURES): cv.string,
    vol.Optional(CONF_DATE_FORMAT, default=DEFAULT_DATE_FORMAT): cv.string
})