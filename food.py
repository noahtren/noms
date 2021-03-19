from .client.main import Client
from .client.dict_parse import food_parse
from .objects.nutrient_dict import nutrient_dict
from .objects.food import Meal
from itertools import islice
import copy

def foods(id_value_dict, client):
    # call the client. If more than 25 words are being queried, split it up
    if len(id_value_dict.keys()) > 25:
        print("Must call the database {} times, this may take a couple moments. Status: {leng}/{leng}".format(len(id_value_dict.keys())//25+1,leng=len(id_value_dict.keys())))
        dict_copy = id_value_dict.copy()
        food_obj = []
        while len(dict_copy.keys()) > 25:
            current_dict = {}
            items = islice(dict_copy.items(), 25)
            current_dict.update(items)
            call = client.food_query(current_dict.keys())
            food_obj += food_parse(call, nutrient_dict, list(current_dict.values()))
            for key in current_dict.keys():
                del dict_copy[key]
            print("Status: {}/{}".format(len(dict_copy.keys()), len(id_value_dict.keys())))
        call = client.food_query(dict_copy.keys())
        food_obj += food_parse(call, nutrient_dict, list(dict_copy.values()))
        print("Complete!")
    else:
        food_obj = client.food_query(id_value_dict.keys())
        food_obj = food_parse(food_obj, nutrient_dict, list(id_value_dict.values()))
    return food_obj