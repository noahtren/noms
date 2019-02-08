import copy
import operator
from .nutrient_dict import nutrient_dict, index_from_name

class Food:
    def __init__(self, data):
        self.desc = data["food"]["desc"]
        self.nutrients = data["food"]["nutrients"]

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
        for n in range(0, len(self.nutrients)):
            self.nutrients[n]["value"] = round(self.nutrients[n]["value"], 2)
    def sort_by_top(self, n):
        ni = index_from_name(n)
        self.foods.sort(key=lambda f: f.nutrients[ni]["value"], reverse=True)
        
