from noms.service.search import *
from noms.service.food import *
from noms.service.export import *

# Initialize client object with API key
client = Client("OSqKh1X9zs50n17b34ETVtzrWOLRCkq97gd2dgjk")
# Calls the client to search for the specific query, parses it, and prints it
search("Cheese", client, 3)
# Dictionary containing food id:grams, so that the total nutrition can be calculated
seed_foods ={"07945":100,"28312":100,"21272":225,"19088":100,"19057":50,"14400":500,"14429":1200,"18249":120}

# Obtain food objects based on an API call and parse
f = foods(seed_foods, client)
m = meal(f)
export_report(m)

# todo:
# create a master client so it doesn't need to be passed as a parameter
# fix export location, specify it somehow
# allow for arrays of greater than 25 to be used with service.food method