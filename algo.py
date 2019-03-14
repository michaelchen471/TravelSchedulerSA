import requests

def getFBData(location):
	URL = "https://graph.facebook.com/search?type=place"
	token = "806836442983711|YWvsHgfEXTcsa65ZUav4XcEcO00"
	PARAMS = {'center': str(location[0])+","+str(location[1]), "distance" : "1000", 'categories':"['ARTS_ENTERTAINMENT', 'FOOD_BEVERAGE', 'SHOPPING_RETAIL']", 'fields':"name,category_list,location,overall_star_rating,checkins", "access_token" : token}
	r = requests.get(url = URL, params = PARAMS) 
	data = r.json() 
	parsed = []
	for place in data.get('data'):
		if place.get('overall_star_rating') == None:
			parsed.append([place.get('name'), place.get('checkins') / 10000, 120 + getMapQuestData([location[0], location[1]], [place.get('location').get('latitude'), place.get('location').get('longitude')]), place.get('location')])
		else:
			parsed.append([place.get('name'), place.get('overall_star_rating') / 3 * place.get('checkins') / 10000, 120 + getMapQuestData([location[0], location[1]], [place.get('location').get('latitude'), place.get('location').get('longitude')]), place.get('location')])
	return parsed

def getMapQuestData(start, end):
	URL = "https://www.mapquestapi.com/directions/v2/route?"
	PARAMS = {'from':str(start[0])+","+str(start[1]), 'to':str(end[0])+","+str(end[1]), 'key':"HnOmkazm9gzIpfE5JFFSsiOWGlAH2Ro9"}
	r = requests.get(url = URL, params = PARAMS) 
	data = r.json() 
	return data.get('route').get('time')

def knapSack(data, weight):
	n = len(data)

	K = [[0 for x in range(weight + 1)] for x in range(n + 1)] 

	# Build table K[][] in bottom up manner 
	for i in range(n + 1):
		for w in range(weight + 1):
			if i == 0 or w == 0:
				K[i][w] = 0
			elif data[i - 1][2] <= w:
				K[i][w] = max(val[i-1] + K[i-1][w-data[i-1][2]],  K[i-1][w])
			else:
				K[i][w] = K[i-1][w]
	return K[n][weight]

def kmean():


	