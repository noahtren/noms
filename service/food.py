from ..client.main import Client
from ..client.dict_parse import food_parse
from ..objects.nutrient_dict import nutrient_dict
from ..objects.food import Meal

def foods(id_value_dict, client):
    food_obj = client.food_query(id_value_dict.keys())
    # Return list of food objects in context of nutrients being tracked
    food_obj = food_parse(food_obj, nutrient_dict, list(id_value_dict.values()))
    return food_obj

def meal(foods):
    return Meal(foods)