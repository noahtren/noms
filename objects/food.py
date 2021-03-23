import copy
import operator
from .nutrient_dict import nutrient_dict, index_from_name

def norm_rda(nutrient_array, nutrient_dict, disp=False):
    r_nut = copy.deepcopy(nutrient_array)
    if not isinstance(nutrient_dict, (list,)) :
        _nutrient_dict = nutrient_dict()()
    else:
        _nutrient_dict = nutrient_dict
    for ni, _ in enumerate(_nutrient_dict):
        norm_val = 0
        if _nutrient_dict[ni]['rda'] != None:
            if r_nut[ni]['value'] < _nutrient_dict[ni]['rda']:
                # value is 5, rda is 15
                # norm value is 5/15 = 0.33
                r_nut[ni].update(to="rda")
                norm_val = r_nut[ni]['value']/_nutrient_dict[ni]['rda']
            else:
                # value is 30, rda is 15
                # norm value is 1
                r_nut[ni].update(to="rda")
                norm_val = 1
        if _nutrient_dict[ni]['limit'] != None:
            if r_nut[ni]['value'] > _nutrient_dict[ni]['limit']:
                r_nut[ni].update(to="limit")
                norm_val = r_nut[ni]['value']/_nutrient_dict[ni]['limit']
            elif _nutrient_dict[ni]['rda'] == None:
                if disp:
                    r_nut[ni].update(to="limit")
                    norm_val = r_nut[ni]['value']/_nutrient_dict[ni]['limit']
                else:
                    norm_val = 1
        r_nut[ni].update(value=norm_val)
        if 'measures' in r_nut[ni].keys():
            del r_nut[ni]['measures']
        del r_nut[ni]['unit']
    return r_nut

class Food:
    def __init__(self, data):
        self.data = data
        self.desc = data["description"]
        self.nutrients = data["foodNutrients"]
    def norm_rda(self, nutrient_dict):
        return norm_rda(self.nutrients, nutrient_dict)

class Meal:
    def __init__(self, foods):
        self.foods = foods
        self.nutrients = []
        for nutrient in foods[0].nutrients:
            to_app = nutrient.copy()
            to_app["value"] = 0
            self.nutrients.append(to_app)
        for food in foods:
            n = 0
            for nutrient in food.nutrients:
                self.nutrients[n]["value"] += nutrient["value"]
                n += 1
        for ni, _ in enumerate(self.nutrients):
            self.nutrients[ni]["value"] = self.nutrients[ni]["value"]
    def sort_by_top(self, n):
        ni = index_from_name(n)
        self.foods.sort(key=lambda f: f.nutrients[ni]["value"], reverse=True)
    def norm_rda(self, nutrient_dict, disp=False):
        return norm_rda(self.nutrients, nutrient_dict, disp)
