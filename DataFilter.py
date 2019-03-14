from Place import Place
from KMeans import KMeans
import requests
import simulatedAnnealing

class DataFilter:

    def query_potential_locations(self, center_lat, center_lon, num_locations=10, dist=100):
        '''
            Queries num_locations near the center (lat, lon) using Facebook Places API_KEY
        '''

        center = center_lat + ", " + center_lon
        API_KEY = "AIzaSyAJwLS8cN68r1unGA6XWr0OnNCrWSWIdSo"
        access_token = "319423692240891|mvdhdDsaI94iMUGTFTkGAFPp4Fs"
        FB_URL = "https://graph.facebook.com/search?type=place"
        FB_PARAMS = {'categories' : "['FOOD_BEVERAGE','ARTS_ENTERTAINMENT','SHOPPING_RETAIL']", \
            'fields': ['name,checkins,overall_star_rating,location, category_list'], \
            'center': center, \
            'distance': 2000, \
            'access_token': access_token}
        res = requests.get(url = FB_URL, params = FB_PARAMS)
        all_locations = res.json()['data']
        all_locations.sort(key = lambda place: -place['checkins'])
        attractions_with_rating = [a for a in all_locations if 'overall_star_rating' in a]

        return attractions_with_rating[:num_locations]

    def filter_by_popularity(self, center, attractions):
        '''
            Filters attractions using knapsack.
            weights = a weighted average of estimated time spent at location and distance from center
            values = a weighted average of num checkins and overall star rating
        '''
        places, weights, values = [], [], []
        for attraction in attractions:
            place = \
                Place(attraction["name"], \
                    attraction["location"]["latitude"], \
                    attraction["location"]["longitude"], \
                    attraction)
            val = place.calculate_value(attraction["checkins"], attraction["overall_star_rating"])
            weight = place.calculate_weight(center)
            values.append(val)
            weights.append(weight)
            places.append(place)
        return self.knapsack(5000000, weights, values, len(places), places)

    def cluster_attractions(self, data, days):

        '''
            Clusters attractions into the # days clusters.
        '''
        return self.k_means(data, days)

    ################## HELPER FUNCTIONS #######################
    # Performs knapsack on list of weights/values
    def knapsack(self, W, wt, val, n, attractions):
        K = [[0 for x in range(W+1)] for x in range(n+1)]

        # Build table K[][] in bottom up manner
        for i in range(n+1):
            for w in range(W+1):
                if i==0 or w==0:
                    K[i][w] = 0
                elif wt[i-1] <= w:
                    K[i][w] = max(val[i-1] + K[i-1][w-wt[i-1]],  K[i-1][w])
                else:
                    K[i][w] = K[i-1][w]

       # stores the result of Knapsack
        res = K[n][W]
        visited_list = []
        w = W
        for i in range(n, 0, -1):
            if res <= 0:
                break
            if res == K[i - 1][w]:
                continue
            else:
                visited_list.append(attractions[i-1])
                print(attractions[i - 1].name)
                res = res - val[i - 1]
                w = w - wt[i - 1]
        return visited_list

    def k_means(self, data, k=3):
        ''' Runs k means algorithm on data, and returns the clustered data '''
        kmeans = KMeans(k)
        kmeans.fit(data)
        return kmeans.classification_names

center = "40.7304, -73.9921"
dataFilter = DataFilter()
attractions = dataFilter.query_potential_locations("40.7304", "-73.9921")
filtered_attractions = dataFilter.filter_by_popularity(center, attractions)
clustered_attractions = dataFilter.cluster_attractions(filtered_attractions, 3)
print(type(clustered_attractions[0][0]))
print(clustered_attractions)

print(simulatedAnnealing.simulatedAnnealing(clustered_attractions, center))