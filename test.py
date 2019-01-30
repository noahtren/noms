from noms.client.main import Client
key = open("key.txt","r").read()
client = Client(key)

from noms.service.search import get_results, print_results
from noms.service.food import foods, meal
from noms.service.export import export_report

print_results(get_results("Raw Broccoli", client))