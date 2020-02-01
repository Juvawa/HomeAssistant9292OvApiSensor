import constants
import http.client
import logging

from homeassistant.util import Throttle
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_RESOURCE = 'api.9292.nl/0.1'
_LOGGER = logging.getLogger(__name__)


class OvApiData:
    def __init__(self, location):
        self._resource = _RESOURCE
        self._location = location
        self.result = ""
        self._headers = {
            'cache-control': "no-cache",
            'accept': "application/json"
        }

    @Throttle(constants.MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        if self._location == constants.CONF_LOCATION:
            _LOGGER.error("Impossible to get data from 9292OV Api, no location.")
            self.result = "Impossible to get data from 9292OV Api, no location."
        else:
            try:
                response = http.client.HTTPConnection(self._resource, timeout=1)
                response.request("GET", "/locations/" + self._location + "/departure_times?lang=nl_NL",
                                 headers=self._headers)
                result = response.getresponse()
                self.result = result.read().decode('utf-8')
            except http.client.HTTPException:
                _LOGGER.error("Impossible to get data from 929OV Api using location.")
                self.result = "Impossible to get data from 929OV Api using location."
