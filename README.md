# Google GeoCode App

## Overview

Google GeoCode app is a way to translate your address fields into (latitude,longitude). If you do not have IP address in your data and still want to use the map with markers, this app will help you. 

# Installation

  - Install the app on your search head
  - Get a google API key from [Google API Key](https://developers.google.com/maps/documentation/javascript/get-api-key)
  - Write the API_Key in the myconfig.py file under bin directory
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


