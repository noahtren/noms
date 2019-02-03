import copy

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
