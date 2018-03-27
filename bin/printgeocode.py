import splunk.Intersplunk
import requests

def geocode(string):

	address=string
	# API_KEY From Google, to be added in appsetup.conf file
	fname = open('../local/appsetup.conf', 'r')
	for line in fname.readlines():
		if '=' not in line:
			continue
		l = line.strip().split('=')
		api_key_val=l[1]
			
	lat=None
	lon=None
	url='https://maps.googleapis.com/maps/api/geocode/json'
	params={'sensor':'false','address':address,'key':api_key_val}
	r=requests.get(url,params=params)
	status=r.json()['status']
	if status == 'OK':
		d=dict(r.json())
		loc=d['results'][0]['geometry']['location']
		lat,lon=loc['lat'],loc['lng']
	else:
		lat=None
		lon=None
	return status,lat,lon
	

def reverse_geocode(lat,lon):
	
	fname = open('../local/appsetup.conf', 'r')
	for line in fname.readlines():
		if '=' not in line:
			continue
		l = line.strip().split('=')
		api_key_val=l[1]

	# Reverse Geocoding
	base='https://maps.googleapis.com/maps/api/geocode/json?'
	params="latlng={lat},{lon}&sensor={sen}&key={key}".format(
		lat=lat,
		lon=lon,
		sen='false',
		key=api_key_val
	)
	url="{base}{params}".format(base=base,params=params)
	r=requests.get(url)
	status=r.json()['status']
	if status == 'OK':
		d=dict(r.json())
		address=d['results'][0]['formatted_address']
	else:
		address=None
	return status,address
 
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
				status_field = "geolocation_status"
				address_value = result[address]
				status,lat,lng = geocode(address_value)
				if status == 'OK':
					result[status_field]=status
					result[newfield1]=lat
					result[newfield2]=lng
				else:
					result[status_field]=status
					result[newfield1]="NA"
					result[newfield2]="NA"
			if Type == "reverse":
				newfield = "geolocation_addr"
				lat_value = result[lat]
				lon_value = result[lon]
				status_field = "geolocation_status"
				status,address=reverse_geocode(lat_value,lon_value)
				if status == 'OK':
					result[newfield] = address
					result[status_field]=status
				else:
					result[newfield] = None
					result[status_field]=status
     # Let the modified events flow back into the search results
		splunk.Intersplunk.outputResults(results)
 
	except:
		import traceback
		stack =  traceback.format_exc()
 
 # Get the events from splunk
results, dummyresults, settings = splunk.Intersplunk.getOrganizedResults()
 # Send the events to be worked on
results = customcommand(results, settings)
