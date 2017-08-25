# Google GeoCode App

## Overview

Google GeoCode app is a way to translate your address fields into (latitude,longitude). If you do not have IP address in your data and still want to use the map with markers, this app will help you.

Version: 1.2

# Infrastructure Requiment

Any Operating system (tested on Windows 10 and Linux)
Splunk 6.5

# Installation

  - Install the app on your search head
  - Get a google API key from [Google API Key](https://developers.google.com/maps/documentation/javascript/get-api-key)
  - Write the API_Key in the setup page
  - Pass your address field to command and see the magic!

# Usage
```sh
  <your splunk query>|printgeocode address
 ```
  Where address is the name of the text field in your data which contains a valid address. For example:

 ```sh
index=_internal | stats count by source |eval Address="San Jose, California, United States" | printgeocode Address
```

 As simple as looking for a location on Maps, don't you think?

You can also:
  - Add simple rex and eval to extract lat and long values and then plot a map
  - Use other apps which plot multiple markers

### Troubleshooting

- If you do not get any results after printgeocode but your query is working fine otherwise, it means that probably you have exhaused the daily request limit (2500 requests per day) for free version.
--  Option1: Get a new Key and put that value in myconfig.py. Restart Splunk search head, the results should be good.
-- Option 2: Wait for midnight PST timezone for the limit to rest :)


More information and code is avaialble here:

[Gitgub Link](https://github.com/meenalluktuke/GoogleGeoCode/blob/master/README.md)

# References
The app uses the geopy Python library. Here's the link to their [documentation](https://pypi.python.org/pypi/geopy)

geopy is a Python 2 and 3 client for several popular geocoding web services.
geopy makes it easy for Python developers to locate the coordinates of addresses, cities, countries, and landmarks across the globe using third-party geocoders and other data sources.

geopy is tested against CPython 2.7, CPython 3.2, CPython 3.4, PyPy, and PyPy3.

The app uses version 1.11.0 of the geopy library.
Github link for the project - [Github Link](https://github.com/geopy/geopy)


# Contact Information
For any issues or questions, please reach out to: meenal.luktuke@gmail.com
We provide only Level-1 support for this application.
