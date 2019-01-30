# Nutrient Object Management System (noms)

noms is a fun and simple Python package to obtain and work with highly detailed nutrition data for nearly 8,000 entries from the USDA Standard Reference Food Composition Database. The Standard Reference Database is used explicitly without the addition of their Branded Foods database, as only the former allows for highly detailed reports which track nearly 200 different nutrients -- much more information than you would find on an item's nutrition facts! This is especially valuable for nutritionists or people interested in their own health to explore the nutritional content of whole foods. 

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

##To-Do
Allow the foods() method from the noms.service.food module to accept dictionaries of length greater than 25. It currently maxes out at this value because the API only accepts calls of this size.