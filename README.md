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
from noms.service.food import foods
from noms.service.search import get_results, print_results
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
Broccoli, raw                                                            Vegetables and Vegetable Pro..    11090
Broccoli raab, raw                                                       Vegetables and Vegetable Pro..    11096
Broccoli, leaves, raw                                                    Vegetables and Vegetable Pro..    11739
Broccoli, stalks, raw                                                    Vegetables and Vegetable Pro..    11741
Broccoli, chinese, raw                                                   Vegetables and Vegetable Pro..    11994
Broccoli, flower clusters, raw                                           Vegetables and Vegetable Pro..    11740
================================================================================================================
```

## To-Do
1. Allow the foods() method from the noms.service.food module to accept dictionaries of length greater than 25. (It currently maxes out at this value because the API only accepts calls of this size.)
2. Display column labels in print_results
3. Complete README.md