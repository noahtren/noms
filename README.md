# Nutrient Object Management System (noms)

Note: I'm not able to maintain this package right now, so there is a chance that the current API integration is broken/will break given the new FoodData Central API from the USDA.

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
Name                                                                                 Group                    ID
Broccoli, raw                                                            Vegetables and Vegetable Pro..    11090
Broccoli raab, raw                                                       Vegetables and Vegetable Pro..    11096
Broccoli, leaves, raw                                                    Vegetables and Vegetable Pro..    11739
Broccoli, stalks, raw                                                    Vegetables and Vegetable Pro..    11741
Broccoli, chinese, raw                                                   Vegetables and Vegetable Pro..    11994
Broccoli, flower clusters, raw                                           Vegetables and Vegetable Pro..    11740
================================================================================================================
```
## Requesting Food Data From the Database
In this example, the ids correlate with Raw Broccoli (11090) and a Cola Beverage (14400). The numbers afterwards represent the mass of that food, in grams. More mass for a given food equals a greater amount of each nutrient in equal proportion (twice the broccoli has twice the vitamins).
```python
food_list = client.get_foods({'11090':100, '14400':100})
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
{'name': 'Protein', 'rda': 125.0, 'limit': None, 'value': 2.89, 'state': 'deficient', 'unit': 'g'}
{'name': 'Fat', 'rda': 55.56, 'limit': None, 'value': 0.39, 'state': 'deficient', 'unit': 'g'}
{'name': 'Carbs', 'rda': 250.0, 'limit': None, 'value': 16.2, 'state': 'deficient', 'unit': 'g'}
{'name': 'Calories', 'rda': 2000, 'limit': None, 'value': 71.0, 'state': 'deficient', 'unit': 'kcal'}
{'name': 'Water', 'rda': 2000, 'limit': None, 'value': 179.61, 'state': 'deficient', 'unit': 'g'}
{'name': 'Caffeine', 'rda': 0, 'limit': 400, 'value': 8.0, 'state': 'satisfactory', 'unit': 'mg'}
{'name': 'Theobromine', 'rda': 0, 'limit': 300, 'value': 0.0, 'state': 'satisfactory', 'unit': 'mg'}
{'name': 'Sugar', 'rda': 0, 'limit': 50.0, 'value': 10.67, 'state': 'satisfactory', 'unit': 'g'}
{'name': 'Fiber', 'rda': 28.0, 'limit': None, 'value': 2.6, 'state': 'deficient', 'unit': 'g'}
{'name': 'Calcium', 'rda': 1000, 'limit': 2500, 'value': 49.0, 'state': 'deficient', 'unit': 'mg'}
{'name': 'Iron', 'rda': 8, 'limit': 45, 'value': 0.84, 'state': 'deficient', 'unit': 'mg'}
{'name': 'Magnesium', 'rda': 300, 'limit': 700, 'value': 21.0, 'state': 'deficient', 'unit': 'mg'}
{'name': 'Phosphorus', 'rda': 700, 'limit': 4000, 'value': 76.0, 'state': 'deficient', 'unit': 'mg'}
{'name': 'Potassium', 'rda': 1400, 'limit': 6000, 'value': 318.0, 'state': 'deficient', 'unit': 'mg'}
{'name': 'Sodium', 'rda': 1000, 'limit': 2300, 'value': 37.0, 'state': 'deficient', 'unit': 'mg'}
{'name': 'Zinc', 'rda': 12, 'limit': 100, 'value': 0.43, 'state': 'deficient', 'unit': 'mg'}
{'name': 'Copper', 'rda': 0.9, 'limit': 10, 'value': 0.05, 'state': 'deficient', 'unit': 'mg'}
{'name': 'Fluoride', 'rda': 400, 'limit': 10000, 'value': 57.0, 'state': 'deficient', 'unit': 'µg'}
{'name': 'Manganese', 'rda': 1.8, 'limit': None, 'value': 0.21, 'state': 'deficient', 'unit': 'mg'}
{'name': 'Selenium', 'rda': 70, 'limit': 400, 'value': 2.6, 'state': 'deficient', 'unit': 'µg'}
{'name': 'Vitamin A', 'rda': 900, 'limit': 20000, 'value': 623.0, 'state': 'deficient', 'unit': 'IU'}
{'name': 'Vitamin E', 'rda': 15, 'limit': 1000, 'value': 0.78, 'state': 'deficient', 'unit': 'mg'}
{'name': 'Vitamin D', 'rda': 1000, 'limit': 8000, 'value': 0.0, 'state': 'deficient', 'unit': 'IU'}
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
{'nutrient_id': 269, 'name': 'Sugar', 'group': 'Proximates', 'unit': 'g', 'value': 8.97}
{'nutrient_id': 269, 'name': 'Sugar', 'group': 'Proximates', 'unit': 'g', 'value': 1.7}
```
Note that this sorts the foods in the Meal object from greatest to least in terms of how much sugar each food has.

## Generate Food Recommendations in Context of a Meal and Pantry
Because it would be computationally expensive to generate a food recommendation in the context of every food in the database, and it may be unrealistic to recommend any food from the database as it may be hard to access, you must define a list of foods that will serve as a pantry object. Here is an example pantry object containing many common whole foods.

```python
    pantry = {
    # DAIRY AND EGG
    "01001":100, # butter, salted
    "01145":100, # butter, without salt
    "01079":100, # 2% milk
    "01077":100, # milk, whole
    "01086":100, # skim milk
    "01132":100, # scrambled eggs
    "01129":100, # hard boiled eggs
    "01128":100, # fried egg
    # MEAT
    "15076":100, # atlantic salmon
    "07935":100, # chicken breast oven-roasted
    "13647":100, # steak
    "05192":100, # turkey
    # FRUIT
    "09037":100, # avocado
    "09316":100, # strawberries
    "09050":100, # blueberry
    "09302":100, # raspberry
    "09500":100, # red delicious apple
    "09040":100, # banana
    "09150":100, # lemon
    "09201":100, # oranges
    "09132":100, # grapes
    # PROCESSED
    "21250":100, # hamburger
    "21272":100, # pizza
    "19088":100, # ice cream
    "18249":100, # donut
    # DRINK
    "14400":100, # coke
    "14429":100, # tap water
    "14433":100, # bottled water
    "09206":100, # orange juice
    "14278":100, # brewed green tea
    "14209":100, # coffee brewed with tap water
    # (milk is included in dairy group)
    # GRAIN
    "12006":100, # chia
    "12220":100, # flaxseed
    "20137":100, # quinoa, cooked
    "20006":100, # pearled barley
    "20051":100, # white rice enriched cooked
    "20041":100, # brown rice cooked
    "12151":100, # pistachio
    "19047":100, # pretzel
    "12061":100, # almond
    # LEGUME
    "16057":100, # chickpeas
    "16015":100, # black beans
    "16043":100, # pinto beans
    "16072":100, # lima beans
    "16167":100, # peanut butter smooth
    # VEGETABLE
    "11124":100, # raw carrots
    "11090":100, # broccoli
    "11457":100, # spinach, raw
    "11357":100, # baked potato
    "11508":100, # baked sweet potato
    "11530":100, # tomato, red, cooked
    "11253":100, # lettuce
    "11233":100, # kale
    "11313":100, # peas
    "11215":100, # garlic
    # OTHER
    "04053":100, # olive oil
    "19904":100, # dark chocolate
    "11238":100, # shiitake mushrooms
    "19165":100, # cocoa powder
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
    print(str(round(rec[2] * 100, 2)) + "g", "of", pantry_food[rec[1]].desc["name"])
```
```
50.36g of Seeds, chia seeds, dried
53.3g of Nuts, almonds
56.76g of Peanut Butter, smooth (Includes foods for USDA's Food Distribution Program)
```
It is reasonable that the function returned these foods from the pantry as the current daily nutrition is low in protein and Omega-3s, which chia seeds satisfy the most.
