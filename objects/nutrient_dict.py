import json
import os
import codecs

def index_from_name(name):
    i = 0
    _nutrient_dict = nutrient_dict()()
    for nutrient in _nutrient_dict:
        if nutrient["name"] == name:
            return i
        if "nickname" in nutrient.keys():
            if nutrient["nickname"] == name:
                return i
        i += 1
    # if not found, return -1
    return -1

class nutrient_dict:
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        nutrient_file = codecs.open("{}/nutrient_ids.json".format(dir_path), encoding="utf-8").read()
        nutrient_dict = json.loads(nutrient_file)

        # PROFILE INFORMATION
        tdee = 2000 #kcal per day
        # What percent of daily caloric intake should each macro take?
        protein_p = 0.25
        carb_p = 0.50
        fat_p = 0.25
        # Sugar should be no more than 10% of total calories
        # US dietary guidelines: https://health.gov/dietaryguidelines/2015/guidelines/executive-summary/
        sugar_p = 0.10

        # Assign RDAs, some dependent on gender or tdee
        for item in nutrient_dict:
            id = item["nutrient_id"]
            # PROXIMATES
            if id == 203: # Protein, g
                item.update(rda=(tdee/4)*protein_p)
            if id == 204: # Fat, g
                item.update(rda=(tdee/9)*fat_p)
            if id == 205: # Carbs, g
                item.update(rda=(tdee/4)*carb_p)
            if id == 207: # Ash, g
                item.update(rda=None)
            if id == 208: # Calories, kcal
                item.update(rda=tdee)
            if id == 221: # Alcohol, g note: 7 calories per gram
                item.update(rda=None)
            if id == 255: # Water, g
                item.update(rda=2000)
            # OTHER
            if id == 262: # Caffeine, mg
                item.update(rda=None)
                item.update(limit=400)
            if id == 263: # Theobromine, mg
                item.update(rda=None)
                item.update(limit=300)
            # PROXIMATES
            if id == 269: # Sugar, g
                item.update(rda=None)
                item.update(limit=(tdee/4)*sugar_p)
            if id == 291: # Fiber, g note: 14 grams for every 1000 calories
                item.update(rda=tdee*0.014)
            # MINERALS
            if id == 301: # Calcium, mg
                item.update(rda=1000)
                item.update(limit=2500)
            if id == 303: # Iron, mg
                item.update(rda=8)
                item.update(limit=45)
            if id == 304: # Magnesium, mg
                item.update(rda=300)
                item.update(limit=700)
            if id == 305: # Phosphorus, mg
                item.update(rda=700)
                item.update(limit=4000)
            if id == 306: # Potassium, mg
                item.update(rda=1400)
                item.update(limit=6000)
            if id == 307: # Sodium, mg
                item.update(rda=1000)
                item.update(limit=2300)
            if id == 309: # Zinc, mg
                item.update(rda=12)
                item.update(limit=100)
            if id == 312: # Copper, mg
                item.update(rda=0.9)
                item.update(limit=10)
            if id == 313: # Fluoride, ug
                item.update(rda=400)
                item.update(limit=10000)
            if id == 315: # Manganese, mg
                item.update(rda=1.8)
            if id == 317: # Selenium, ug
                item.update(rda=70)
                item.update(limit=400)
            # VITAMINS
            if id == 318: # Vitamin A, IU
                item.update(rda=900)
                item.update(limit=20000)
            if id == 323: # Vitamin E, mg
                item.update(rda=15)
                item.update(limit=1000)
            if id == 324: # Vitamin D, IU
                item.update(rda=1000)
                item.update(limit=8000)
            if id == 401: # Vitamin C, mg
                item.update(rda=90)
                item.update(limit=2000)
            if id == 404: # Vitamin B-1, mg
                item.update(rda=1.2)
            if id == 405: # Vitamin B-2, mg
                item.update(rda=1.3)
            if id == 406: # Vitamin B-3, mg
                item.update(rda=16)
            if id == 410: # Vitamin B-5, mg
                item.update(rda=4)
            if id == 415: # Vitamin B-6, mg
                item.update(rda=1.3)
                item.update(limit=100)
            if id == 417: # Vitamin B-9, ug
                item.update(rda=400)
                item.update(limit=1000)
            if id == 418: # Vitamin B-12, mg
                item.update(rda=2.4)
            if id == 421: # Choline, mg
                item.update(rda=550)
                item.update(limit=3500)
            if id == 430: # Vitamin K, ug
                item.update(rda=120)
            # LIPIDS
            if id == 601: # Cholesterol, mg
                item.update(rda=None)
                item.update(limit=300)
            if id == 605: # Trans Fat, g
                item.update(rda=None)
                # avoid more than 5% of fat calories from trans fat
                item.update(limit=(tdee/9)*(fat_p*0.05))
            if id == 606: # Saturated Fat, g
                item.update(rda=None)
                item.update(limit=(tdee/9)*(fat_p*0.3))
            if id == 621: # DHA, g
                item.update(rda=0.5)
            if id == 629: # EPA, g
                item.update(rda=0.5)
            if id == 645: # Monounsaturated Fat, g
                item.update(rda=(tdee/9)*(fat_p*.40))
            if id == 646: # Polyunsaturated Fat, g
                item.update(rda=(tdee/9)*(fat_p*.30))
            if id == 851: # ALA, g
                item.update(rda=0.6)
            if "limit" not in item.keys():
                item.update(limit=None)

        # Round values to avoid long decimals in rda values
        for item in nutrient_dict:
            if item["rda"] != None:
                item["rda"] = round(item["rda"], 2)
            if item["limit"] != None:
                item["limit"] = round(item["limit"], 2)
        self.nutrient_dict = nutrient_dict
    def __call__(self):
        return self.nutrient_dict
