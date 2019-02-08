# Nutrient Object Management System (noms)

noms is a fun and simple Python package that allows you to obtain and work with highly detailed nutrition data for nearly 8,000 entries from the USDA Standard Reference Food Composition Database. No mainstream nutrition tracker apps reflect the level of detail that the USDA has compiled. With noms you can track:
1. "Proximates" including macronutrients, calories, fiber and water content
2. 11 minerals
3. 13 vitamins including all of the B vitamins and choline
4. Specific lipids including EPA and DHA (the most important omega-3s found in fish oil)
This amounts to 41 nutrients being tracked, but many more are available from the database such as amino acids and other lipids. These can be viewed in all_nutrient_ids.txt, and support for other nutrients will be added in the future as requested.

Note: The Standard Reference Database is used explicitly without the addition of the USDA's Branded Foods database, as only the former allows for highly detailed reports which track nearly 200 different nutrients -- much more information than you would find on an item's nutrition facts! This is especially valuable for nutritionists or people interested in their own health to explore the nutritional content of whole foods. 

## Installation
noms is not yet on PyPI so it cannot be installed through pip. For now, you can download or clone this repository and import it from the same directory that the test.py file is in.

## How to Use
1. Get a data.gov API key for free from here: https://api.data.gov/signup/
2. Initialize a client object with the key you received.
```python
from noms.client.main import Client
client = Client("api key")
```
3. Import the methods that you'd like to use from the services subpackage.
```python
from noms.service.search import get_results, print_results
from noms.service.food import foods
```
4. Using the search module.
```python
search_results = get_results("Raw Broccoli", client)
print_results(search_results)
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
5. Requesting food data from the database. In this example, the ids correlate with Raw Broccoli (11090) and a Cola Beverage (14400). The numbers afterwards represent the mass of that food, in grams. More mass for a given food equals a greater amount of each nutrient in equal proportion (twice the broccoli has twice the vitamins).
```python
food_list = foods({'11090':100, '14400':100}, client)
m = meal(food_list)
```
6. Generate and display a report. The report is a Python dictionary with attributes based on the meal object and the nutrient_dict object from noms.objects.nutrient_dict. This is where the RDAs and limits for each nutrient are recorded.
```python
r = report(m)
for i in r:
    print(i)
```
```
{'name': 'Protein', 'rda': 125.0, 'limit': None, 'value': 2.89, 'state': 'deficient'}
{'name': 'Fat', 'rda': 55.56, 'limit': None, 'value': 0.39, 'state': 'deficient'}
{'name': 'Carbs', 'rda': 250.0, 'limit': None, 'value': 16.2, 'state': 'deficient'}
{'name': 'Calories', 'rda': 2000, 'limit': None, 'value': 71.0, 'state': 'deficient'}
{'name': 'Water', 'rda': 2000, 'limit': None, 'value': 179.61, 'state': 'deficient'}
{'name': 'Caffeine', 'rda': 0, 'limit': 400, 'value': 8.0, 'state': 'satisfactory'}
{'name': 'Theobromine', 'rda': 0, 'limit': 300, 'value': 0.0, 'state': 'satisfactory'}
{'name': 'Sugar', 'rda': 0, 'limit': 50.0, 'value': 10.67, 'state': 'satisfactory'}
{'name': 'Fiber', 'rda': 28.0, 'limit': None, 'value': 2.6, 'state': 'deficient'}
{'name': 'Calcium', 'rda': 1000, 'limit': 2500, 'value': 49.0, 'state': 'deficient'}
{'name': 'Iron', 'rda': 8, 'limit': 45, 'value': 0.84, 'state': 'deficient'}
{'name': 'Magnesium', 'rda': 300, 'limit': 700, 'value': 21.0, 'state': 'deficient'}
{'name': 'Phosphorus', 'rda': 700, 'limit': 4000, 'value': 76.0, 'state': 'deficient'}
{'name': 'Potassium', 'rda': 1400, 'limit': 6000, 'value': 318.0, 'state': 'deficient'}
{'name': 'Sodium', 'rda': 1000, 'limit': 2300, 'value': 37.0, 'state': 'deficient'}
{'name': 'Zinc', 'rda': 12, 'limit': 100, 'value': 0.43, 'state': 'deficient'}
{'name': 'Copper', 'rda': 0.9, 'limit': 10, 'value': 0.05, 'state': 'deficient'}
{'name': 'Fluoride', 'rda': 400, 'limit': 10000, 'value': 57.0, 'state': 'deficient'}
{'name': 'Manganese', 'rda': 1.8, 'limit': None, 'value': 0.21, 'state': 'deficient'}
{'name': 'Selenium', 'rda': 70, 'limit': 400, 'value': 2.6, 'state': 'deficient'}
{'name': 'Vitamin A', 'rda': 900, 'limit': 20000, 'value': 623.0, 'state': 'deficient'}
{'name': 'Vitamin E', 'rda': 15, 'limit': 1000, 'value': 0.78, 'state': 'deficient'}
{'name': 'Vitamin D', 'rda': 1000, 'limit': 8000, 'value': 0.0, 'state': 'deficient'}
{'name': 'Vitamin C', 'rda': 90, 'limit': 2000, 'value': 89.2, 'state': 'deficient'}
{'name': 'Vitamin B-1', 'rda': 1.2, 'limit': None, 'value': 0.07, 'state': 'deficient'}
{'name': 'Vitamin B-2', 'rda': 1.3, 'limit': None, 'value': 0.12, 'state': 'deficient'}
{'name': 'Vitamin B-3', 'rda': 16, 'limit': None, 'value': 0.64, 'state': 'deficient'}
{'name': 'Vitamin B-5', 'rda': 4, 'limit': None, 'value': 0.57, 'state': 'deficient'}
{'name': 'Vitamin B-6', 'rda': 1.3, 'limit': 100, 'value': 0.17, 'state': 'deficient'}
{'name': 'Vitamin B-9', 'rda': 400, 'limit': 1000, 'value': 63.0, 'state': 'deficient'}
{'name': 'Vitamin B-12', 'rda': 2.4, 'limit': None, 'value': 0.0, 'state': 'deficient'}
{'name': 'Choline', 'rda': 550, 'limit': 3500, 'value': 19.0, 'state': 'deficient'}
{'name': 'Vitamin K', 'rda': 120, 'limit': None, 'value': 101.6, 'state': 'deficient'}
{'name': 'Cholesterol', 'rda': 0, 'limit': 300, 'value': 0.0, 'state': 'satisfactory'}
{'name': 'Trans Fat', 'rda': 0, 'limit': 2.78, 'value': 0.0, 'state': 'satisfactory'}
{'name': 'Saturated Fat', 'rda': 0, 'limit': 16.67, 'value': 0.11, 'state': 'satisfactory'}
{'name': 'DHA', 'rda': 0.5, 'limit': None, 'value': 0.0, 'state': 'deficient'}
{'name': 'EPA', 'rda': 0.5, 'limit': None, 'value': 0.0, 'state': 'deficient'}
{'name': 'Monounsaturated Fat', 'rda': 22.22, 'limit': None, 'value': 0.03, 'state': 'deficient'}
{'name': 'Polyunsaturated Fat', 'rda': 16.67, 'limit': None, 'value': 0.11, 'state': 'deficient'}
{'name': 'ALA', 'rda': 0.6, 'limit': None, 'value': 0.0, 'state': 'deficient'}
```
## To-Do
1. Allow the foods() method from the noms.service.food module to accept dictionaries of length greater than 25. (It currently maxes out at this value because the API only accepts calls of this size.)
2. Add a search method to noms.service.search that returns a dictionary instead of printing a report of search results.