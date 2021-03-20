# Nutrient Object Management System (noms)

Code adatped to accomodate the new FoodData Central API from the USDA.

noms is a fun and simple Python package that allows you to obtain and work with highly detailed nutrition data for nearly 8,000 entries from the USDA Standard Reference Food Composition Database. No mainstream nutrition tracker apps reflect the level of detail that the USDA has compiled. With noms you can track:
1. Proximates including macronutrients (protein, carbs, and fat), calories, fiber and water content
2. 11 minerals
3. 13 vitamins
4. Specific lipids including EPA and DHA (the most important omega-3s found in fish oil)

This amounts to 41 nutrients being tracked, but many more are available from the database such as amino acids and other lipids. These can be viewed in all_nutrient_ids.txt, and support for other nutrients will be added in the future as requested. You can add support for these yourself by editing noms/objects/nutrient_ids.json accordingly with entries from all_nutrient_ids.txt.

Note: The Standard Reference Database is used explicitly without the addition of the USDA's Branded Foods database, as only the former allows for highly detailed reports which track 168 different nutrients -- much more information than you would find on an item's nutrition facts! This is especially valuable for nutritionists or people interested in their own health to explore the nutritional content of whole foods.

## Installation
The noms package is listed on PyPI and can be installed with pip. Simply do:
```
pip install noms
```
If you already have it installed and want to upgrade to the most recent version, do:
```
pip install noms --upgrade
```

## Getting Started
1. Get a data.gov API key for free from here: https://api.data.gov/signup/
2. Initialize a client object with the key you received.
```python
import noms
client = noms.Client("api key")
```
## Searching the Database
```python
search_results = client.search_query("Raw Broccoli")
print(search_results)
```
```
================================================================================================================
Search results for 'Raw Broccoli' on USDA Standard Reference Database
================================================================================================================
description                                                                         dataType                  ID
Broccoli, raw                                                                      Foundation             747447
Broccoli, raw                                                                      SR Legacy              170379
Broccoli raab, raw                                                                 SR Legacy              170381
Broccoli, chinese, raw                                                             SR Legacy              169404
Broccoli, leaves, raw                                                              SR Legacy              169329
Broccoli, stalks, raw                                                              SR Legacy              169331
Broccoli, flower clusters, raw                                                     SR Legacy              169330
Broccoli, raw                                                                    Survey (FNDDS)          1103170
Broccoli raab, raw                                                               Survey (FNDDS)          1103084
Broccoli, chinese, raw                                                           Survey (FNDDS)          1103184
================================================================================================================
```
## Requesting Food Data From the Database
In this example, the ids correlate with Raw Broccoli (11090) and a Cola Beverage (14400). The numbers afterwards represent the mass of that food, in grams. More mass for a given food equals a greater amount of each nutrient in equal proportion (twice the broccoli has twice the vitamins).
```python
search_results = client.get_foods({'747447':100, '174826':100})
```
## Initializing a Meal With a List of Foods
The foods() method returned a list of two Food objects when given the arguments above, but if you would like to generate a report, analyze or sort a group of foods, they should be merged into a Meal object. This is done by simply constructing a Meal instance with a list of Food objects.
```python
m = noms.Meal(food_list)
```

## Generating and Displaying a Report
The report is a dictionary which shows if RDAs (or Adequate Intakes) are being met or exceeded. These values are assigned by default in noms.objects.nutrient_dict, but support will be added to modify these settings in the future.
```python
r = noms.report(m)
for i in r:
    print(i)
```
```
{'name': 'Protein', 'rda': 125.0, 'limit': None, 'value': 2.57, 'state': 'deficient', 'unit': 'g'}
{'name': 'Fat', 'rda': 55.56, 'limit': None, 'value': 0.34, 'state': 'deficient', 'unit': 'g'}
{'name': 'Carbs', 'rda': 250.0, 'limit': None, 'value': 7.3999999999999995, 'state': 'deficient', 'unit': 'g'}
{'name': 'Calories', 'rda': 2000, 'limit': None, 'value': 31.0, 'state': 'deficient', 'unit': 'kcal'}
{'name': 'Water', 'rda': 2000, 'limit': None, 'value': 188.87, 'state': 'deficient', 'unit': 'g'}
{'name': 'Caffeine', 'rda': 0, 'limit': 400, 'value': 0.0, 'state': 'satisfactory', 'unit': 'mg'}
{'name': 'Theobromine', 'rda': 0, 'limit': 300, 'value': 0.0, 'state': 'satisfactory', 'unit': 'mg'}
{'name': 'Sugar', 'rda': 0, 'limit': 50.0, 'value': 0.0, 'state': 'satisfactory', 'unit': 'g'}
{'name': 'Fiber', 'rda': 28.0, 'limit': None, 'value': 2.4, 'state': 'deficient', 'unit': 'g'}
{'name': 'Calcium', 'rda': 1000, 'limit': 2500, 'value': 46.0, 'state': 'deficient', 'unit': 'mg'}
... continued
```
## Sorting Foods in a Meal By a Specific Nutrient
Sometimes it is helpful to see which foods contain the most of a given nutrient in a meal. For example, you may want to see which foods contributed the most sugar for a given day. This can be achieved through the following code:
```python
# index_from_name returns the index that nutrient information exists in an array of nutrients
m.sort_by_top("Sugar")
ni = noms.index_from_name("Sugar")
for food in m.foods:
    print(food.nutrients[ni])
```
```
{'nutrient_id': 269, 'name': 'Sugar', 'group': 'Proximates', 'unit': 'g', 'value': 0.0}
{'value': 0.0, 'name': 'Sugar', 'unit': 'g', 'nutrient_id': 269.0}
```
Note that this sorts the foods in the Meal object from greatest to least in terms of how much sugar each food has.

## Generate Food Recommendations in Context of a Meal and Pantry
Because it would be computationally expensive to generate a food recommendation in the context of every food in the database, and it may be unrealistic to recommend any food from the database as it may be hard to access, you must define a list of foods that will serve as a pantry object. Here is an example pantry object containing many common whole foods.

```python
pantry = {
	   # DAIRY AND EGG
	   "173410":100, # butter, salted
	   "173430":100, # butter, without salt
    	   "1097517":100, # 2% milk
	   "1097512":100, # milk, whole
	   "1097521":100, # skim milk
	   "1100335":100, # scrambled eggs
	   "173424":100, # hard boiled eggs
	   "173423":100, # fried egg
	   # MEAT
	   "175167":100, # atlantic salmon
	   "174608":100, # chicken breast oven-roasted
	   "1099608":100, # steak
	   "1099888":100, # turkey
	   # FRUIT
	   "1103883":100, # avocado
	   "1102710":100, # strawberries
	   "1102702":100, # blueberry
	   "1102708":100, # raspberry
	   "1105430":100, # red delicious apple
	   "173945":100, # banana
	   "1102594":100, # lemon
	   "1102597":100, # oranges
	   "1102665":100, # grapes
	   # PROCESSED
	   "1099796":100, # hamburger
	   "1101112":100, # pizza
	   "1100918":100, # ice cream
	   "174993":100, # donut
	   # DRINK
	   "1104331":100, # coke
	   "1104492":100, # tap water
	   "1104493":100, # bottled water
	   "171354":100, # orange juice
	   "1104292":100, # brewed green tea
	   "171890":100, # coffee brewed with tap water
	   # (milk is included in dairy group)
	   # GRAIN
	   "1100612":100, # chia
	   "1103860":100, # flaxseed
	   "168917":100, # quinoa, cooked
	   "170285":100, # pearled barley
	   "168880":100, # white rice enriched cooked
	   "1101628":100, # brown rice cooked
	   "1100549":100, # pistachio
	   "171370":100, # pretzel
	   "1100555":100, # almond
           # LEGUME
	   "1100429":100, # chickpeas
	   "1100410":100, # black beans
	   "1100393":100, # pinto beans
	   "1100383":100, # lima beans
	   "324860":100 # peanut butter smooth
	   # VEGETABLE
	   "1103193":100, # raw carrots
	   "1103183":100, # broccoli
	   "1103136":100, # spinach, raw
	   "1102880":100, # baked potato
	   "1103261":100, # baked sweet potato
	   "170050":100, # tomato, red, cooked
	   "1103358":100, # lettuce
	   "1103116":100, # kale
	   "1103645":100, # peas
	   "1103845":100, # garlic
	   # OTHER
	   "1103861":100, # olive oil
	   "1104032":100, # dark chocolate
	   "168436":100, # shiitake mushrooms
	   "1097878":100, # cocoa powder
    }
    pantry_food = client.get_foods(pantry)
```
Now, with a list of possible foods to recommend, you can call noms.generate_recommendations with the meal we set up earlier, which consists of just broccoli and brown rice.
```python
recommendations = noms.generate_recommendations(m, pantry_food, noms.nutrient_dict, 3)
for rec in recommendations:
    # a recommendation is a list containing the calculated loss after the recommendation
    # is applied, the index of the pantry for the recommendation, and the amount of that
    # food / 100g
    print(str(round(rec[2] * 100, 2)) + "g", "of", pantry_food[rec[1]].desc)
```
```
72.59g of Chia seeds
72.94g of Almond butter
77.01g of Peanut butter, smooth style, with salt
```
It is reasonable that the function returned these foods from the pantry as the current daily nutrition is low in protein and Omega-3s, which chia seeds satisfy the most.
