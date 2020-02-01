import logging
import constants
import OvApiSensor
import OvApiData

from homeassistant.exceptions import PlatformNotReady

__version__ = '0.1'
_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_entities, discovery_info=None):
    name = config.get(constants.CONF_NAME)
    location = config.get(constants.CONF_LOCATION)
    destination = config.get(constants.CONF_DESTINATION)
    future_departures = config.get(constants.CONF_SHOW_FUTURE_DEPARTURES)

    ov_api = OvApiData(location)

    ov_api.update()

    if ov_api is None:
        raise PlatformNotReady

    sensors = []

    for counter in range(future_departures + 1):
        if counter == 0:
            sensors.append(OvApiSensor(ov_api, name, destination, counter))
        else:
            sensors.append(OvApiSensor(ov_api, name + '_future_' + str(counter), destination, counter))

    add_entities(sensors, True)