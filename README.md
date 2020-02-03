# HomeAssistant9292OvApiSensor

First setup for a Home Assistant sensor using the 9292Ov Api for dutch public transport companies.

##How to install?
Create ```<config_directory>/custom_components/dutch_public_transport_api/``` and copy [these](https://github.com/Juvawa/HomeAssistant9292OvApiSensor/tree/master/custom_components/dutch_public_transport_api) files into the directory.

Example config:
```yaml
sensor:
  - platform: dutch_public_transport_api
    name: Amsterdam naar Vlissingen                     (required)
    station: station-amsterdam-centraal                 (required)
    destination: Vlissingen                             (required)
    show_future_departures: 2                           (optional)
```

#### Name
Name of the sensor

#### Station
The station from where the bus, tram, metro or train should depart. This can be found by following querying the 9292Ov 
API (reference: [Thomas Brus](https://github.com/thomasbrus/9292-api-spec)). The 'id' field of a location will be used as station.

##### Example
_Example query:_
```
GET /0.1/locations?lang=nl-NL&q=amsterdam HTTP/1.1 
Host: api.9292.nl
```
[Example response](http://api.9292.nl/0.1/locations?lang=nl-NL&q=amsterdam)

#### Destination
The destination is equal to the destination of the bus, tram, metro or train. This can be found by following querying the 9292Ov 
API (reference: [Thomas Brus](https://github.com/thomasbrus/9292-api-spec)). The 'destinaton' field of a departure will be 
used as destination. Destination is used for a string compare to find the right departures, make sure it is an exact copy.

_Example query:_
```
GET /0.1/locations/station-amsterdam-centraal/departure-times?lang=nl-NL HTTP/1.1 
Host: api.9292.nl
```
[Example response](http://api.9292.nl/0.1/locations/station-amsterdam-centraal/departure-times?lang=nl-NL)

####Show_future_departures
Number of future departures that should be shown, every future departure is a new sensor.


## Credits:
- [Paul-Dh](https://github.com/Paul-dH) This sensor is based on the sensor of Paul.
- [Thomas Brus](https://github.com/thomasbrus/9292-api-spec) Thanks for figuring the 9292OV Api out, was very useful for this sensor.
