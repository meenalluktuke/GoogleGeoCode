import splunk.Intersplunk
import appconfig
from geopy import geocoders

 
def geocode(string):
  address=string
# API_KEY From Google, to be added in appconfig.py file

  g = geocoders.GoogleV3(api_key=appconfig.api_key)
  place, (lat,lng) = g.geocode(address)
  loc = (lat,lng)
# Returns latitude,longitude pair
  return loc
 
 # A basic shell for any custom streaming command. Just pass the events to it
def customcommand(results, settings):
  try:
    fields, argvals = splunk.Intersplunk.getKeywordsAndOptions()
# This is the field passed with command, has to be a valid address
    address_field = fields[0]
     # Set a default return value
    address_value = "Field does not exist"
     # If the parameter provided exists as a field in the event, run the Geocode math on its value
    for result in results:
       # If field exists in event
      if address_field in result:
         # Get the field's actual value
        address_value = result[address_field]
         # Create the new field we'll place into the events
	# New field will be original fieldname appended with _geolocation
	# For e.g. if fieldname is address, returned field will be addresS_geolocation
        newfield = address_field + "_geolocation"
         # Finally, run the math on the field's value and place it into the newfield we just created
        result[newfield] = geocode(address_value)
 
     # Let the modified events flow back into the search results
    splunk.Intersplunk.outputResults(results)
 
  except:
    import traceback
    stack =  traceback.format_exc()
 
 # Get the events from splunk
results, dummyresults, settings = splunk.Intersplunk.getOrganizedResults()
 # Send the events to be worked on
results = customcommand(results, settings)


