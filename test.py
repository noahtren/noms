from noms.client.main import Client
key = open("key.txt","r").read()
client = Client(key)

from noms.objects.food import Food, Meal
from noms.search import get_results, print_results
from noms.food import foods
from noms.report import export_report, report

print_results(get_results("Raw Broccoli", client))
print_results(get_results("Cola", client))

food_list = foods({'11090':100, '14400':100}, client)
m = Meal(food_list)
r = report(m)
for i in r:
    print(i)

from noms.objects.nutrient_dict import index_from_name

m.sort_by_top("Sugar")
ni = index_from_name("Sugar")
for food in m.foods:
    print(food.nutrients[ni])
