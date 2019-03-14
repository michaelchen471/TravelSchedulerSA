import random

def simulatedAnnealing(data, maxIterations = 100):
	curr = []
	numAttractions = len(data)

	for _ in range(numAttractions):
		rand = random.randint(0, len(data))
		curr.append(data[rand])
		data.remove(data[rand])
		
	bestOrdering = curr
	bestVal = getTime(curr)

	for i in range(maxIterations):
		curr = randomizeOrdering(curr)
		val = getTime(curr)
		if val < bestVal:
			bestVal = val
			bestOrdering = curr

	return bestOrdering

def getTime(data):
	if len(data) < 2:
		return -1
	totalTime = 0
	for i in range(len(data) - 1):
		totalTime += getMapQuestTime(data[i], data[i + 1])
	return totalTime

def getMapQuestTime(start, end):
	URL = "https://www.mapquestapi.com/directions/v2/route?"
	PARAMS = {'from':str(start[0])+","+str(start[1]), 'to':str(end[0])+","+str(end[1]), 'key':"HnOmkazm9gzIpfE5JFFSsiOWGlAH2Ro9"}
	r = requests.get(url = URL, params = PARAMS) 
	data = r.json() 
	return data.get('route').get('time')

def temperature(iteration):
	return 1 / iteration

def randomizeOrdering(data):
	rand1 = random.randint(0, len(data))
	rand2 = random.randint(0, len(data))
	while rand1 == rand2:
		rand2 = random.randint(0, len(data))
	data[rand1], data[rand2] = data[rand2], data[rand1]
	return data

