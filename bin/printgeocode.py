import splunk.Intersplunk
from geopy import geocoders

def geocode(string):

	address=string
	# API_KEY From Google, to be added in appsetup.conf file
	fname = open('../local/appsetup.conf', 'r')
	for line in fname.readlines():
		if '=' not in line:
			continue
		l = line.strip().split('=')
		api_key_val=l[1]
			
	g = geocoders.GoogleV3(api_key=api_key_val)
	place, (lat,lng) = g.geocode(address)

	# Returns latitude,longitude pair
	return lat,lng
	

def reverse_geocode(location):
	Point=location

	fname = open('../local/appsetup.conf', 'r')
	for line in fname.readlines():
		if '=' not in line:
			continue
		l = line.strip().split('=')
		api_key_val=l[1]

	
	# Reverse Geocoding
	g = geocoders.GoogleV3(api_key=api_key_val)
	place = g.reverse(Point,exactly_one=True)
  
        # Returns Address field
	return place.address
 
 # A basic shell for any custom streaming command. Just pass the events to it
def customcommand(results, settings):
	try:
		fields, argvals = splunk.Intersplunk.getKeywordsAndOptions()
		Type = argvals.get('type',None)
		address = argvals.get('address',None)
		lat = argvals.get('latfield',None)
		lon = argvals.get('lonfield',None)

		# Missing arguments validation
		if Type == None:
			splunk.Intersplunk.generateErrorResults("'type' argument required, such as type=geocode or type=reverse")
			exit(0)
		if Type == "geocode":
			if(address == None):
				splunk.Intersplunk.generateErrorResults("String 'address' argument required")
				exit(0)
		if Type == "reverse":
			if lat == None or lon == None:
				splunk.Intersplunk.generateErrorResults("Latitude and Longitude 'latfield,lonfield' arguments required")
				exit(0)

     # If the parameter provided exists as a field in the event, run the Geocode math on its value
		for result in results:
                # Based on the type field, decide whether it's address to lat,long or reverse.
			if Type == "geocode":
				newfield1 = "geolocation_lat"
				newfield2 = "geolocation_lon"

				address_value = result[address]
				lat,lng = geocode(address_value)
				result[newfield1]=lat
				result[newfield2]=lng
			if Type == "reverse":
				newfield = "geolocation_addr"
				lat_value = result[lat]
				lon_value = result[lon]
				loc=lat_value,lon_value
				result[newfield] = reverse_geocode(loc)
     # Let the modified events flow back into the search results
		splunk.Intersplunk.outputResults(results)
 
	except:
		import traceback
		stack =  traceback.format_exc()
 
 # Get the events from splunk
results, dummyresults, settings = splunk.Intersplunk.getOrganizedResults()
 # Send the events to be worked on
results = customcommand(results, settings)


