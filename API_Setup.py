import requests 

#fb

URL = "https://graph.facebook.com/search?type=place"

token = "806836442983711|YWvsHgfEXTcsa65ZUav4XcEcO00"

PARAMS = {"center" : "40.7304,-73.9921", "distance" : "1000", "fields" : "name,checkins,picture", "access_token" : token}

r = requests.get(url = URL, params = PARAMS) 

data = r.json() 

print(data)

#mapquest

URL = "https://www.mapquestapi.com/directions/v2/route?"

PARAMS = {'from':'Clarendon Blvd,Arlington,VA', 'to':"2400SGlebeRd,Arlington,VA", 'ambiguities':"ignore", 'outFormat':"json", 'key':"HnOmkazm9gzIpfE5JFFSsiOWGlAH2Ro9"}

r = requests.get(url = URL, params = PARAMS) 

data = r.json() 

print(data)