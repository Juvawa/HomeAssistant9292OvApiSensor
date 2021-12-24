# HomeAssistant9292OvApiSensor

A Home Assistant sensor using the 9292Ov Api for Dutch public transport companies.

## Installation

### HACS installation (preferred)

The easiest way to install the integration is through [HACS][hacs]. 

First, add [this repository][repo] to [HACS][hacs]:

1. Open HACS from the side panel.
2. Go to any of the sections (integrations, frontend, automation).
3. Click on the 3 dots in the top right corner.
4. Select "Custom repositories".
5. Add the URL to [this repository][repo].
6. Select "Integrations" as the category.
7. Click the "ADD" button.

Next, add the integration to your Home Assistant:

1. Open HACS from the side panel.
2. Go to the sections Integrations.
3. Click the button "Explore % Download Repositories".
4. Search for or scroll to "Sensor 9292 OV API".
5. Select the integration.

Now is the time to add the new platform to your [Configuration](#configuration).

### Manual installation

Create ```<config_directory>/custom_components/dutch_public_transport_api/``` and copy [these](https://github.com/Juvawa/HomeAssistant9292OvApiSensor/tree/master/custom_components/dutch_public_transport_api) files into the directory.

## Configuration

Example config:

```yaml
sensor:
  - platform: dutch_public_transport_api
    name: Amsterdam naar Vlissingen        # (required)
    station: station-amsterdam-centraal    # (required)
    destination: Vlissingen                # (required)
    show_future_departures: 2              # (optional)
```

### name

Name of the sensor

### station

The station from where the bus, tram, metro or train should depart.
This can be found by following querying the 9292Ov API (reference: [Thomas Brus](https://github.com/thomasbrus/9292-api-spec)).
The 'id' field of a location will be used as station.

#### Example

_Example query:_

```text
GET /0.1/locations?lang=nl-NL&q=amsterdam HTTP/1.1 
Host: api.9292.nl
```

[Example response](http://api.9292.nl/0.1/locations?lang=nl-NL&q=amsterdam)

### destination

The destination is equal to the destination of the bus, tram, metro or train.
This can be found by following querying the 9292Ov API (reference: [Thomas Brus](https://github.com/thomasbrus/9292-api-spec)).
The 'destinaton' field of a departure will be used as destination.
Destination is used for a string compare to find the right departures, make sure it is an exact copy.

_Example query:_

```text
GET /0.1/locations/station-amsterdam-centraal/departure-times?lang=nl-NL HTTP/1.1 
Host: api.9292.nl
```

[Example response](http://api.9292.nl/0.1/locations/station-amsterdam-centraal/departure-times?lang=nl-NL)

### show_future_departures

Number of future departures that should be shown, every future departure is a new sensor.

## Credits

- [Paul-Dh](https://github.com/Paul-dH) This sensor is based on the sensor of Paul.
- [Thomas Brus](https://github.com/thomasbrus/9292-api-spec) Thanks for figuring the 9292OV Api out, was very useful for this sensor.

[repo]: https://github.com/Juvawa/HomeAssistant9292OvApiSensor
[hacs]: https://hacs.xyz/