# Nutrient Object Management System (noms)

noms is a fun and simple Python package that allows you to obtain and work with highly detailed nutrition data for nearly 8,000 entries from the USDA Standard Reference Food Composition Database. No mainstream nutrition tracker apps reflect the level of detail that the USDA has compiled. With noms you can track:
1. "Proximates" including macronutrients, calories, fiber and water content
2. 11 minerals
3. 13 vitamins including all of the B vitamins and choline
4. Specific lipids including EPA and DHA (the most important omega-3s found in fish oil)

This amounts to 41 nutrients being tracked, but many more are available from the database such as amino acids and other lipids. These can be viewed in all_nutrient_ids.txt, and support for other nutrients will be added in the future as requested.

Note: The Standard Reference Database is used explicitly without the addition of the USDA's Branded Foods database, as only the former allows for highly detailed reports which track 168 different nutrients -- much more information than you would find on an item's nutrition facts! This is especially valuable for nutritionists or people interested in their own health to explore the nutritional content of whole foods. 

## Installation
noms is not yet on PyPI so it cannot be installed through pip. For now, you can download or clone this repository and imitate the structure of test.py.

## Getting Started
1. Get a data.gov API key for free from here: https://api.data.gov/signup/
2. Initialize a client object with the key you received.
```python
from noms.client.main import Client
client = Client("api key")
```
3. Import the methods that you'd like to use from the services subpackage.
```python
from noms.service.search import get_results, print_results
from noms.service.food import foods, meal
from noms.service.report import export_report, report
```
## Searching the Database
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
## Requesting food data from the database 
In this example, the ids correlate with Raw Broccoli (11090) and a Cola Beverage (14400). The numbers afterwards represent the mass of that food, in grams. More mass for a given food equals a greater amount of each nutrient in equal proportion (twice the broccoli has twice the vitamins).
```python
food_list = foods({'11090':100, '14400':100}, client)
m = meal(food_list)
```
## Generating and displaying a report 
The report is a Python dictionary with attributes based on the meal object and the nutrient_dict object from noms.objects.nutrient_dict. This is where the RDAs and limits for each nutrient are recorded.
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
... continued
```
## To-Do
1. Allow the foods() method from the noms.service.food module to accept dictionaries of length greater than 25. (It currently maxes out at this value because the API only accepts calls of this size.)
2. Add a search method to noms.service.search that returns a dictionary instead of printing a report of search results.