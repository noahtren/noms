import csv
import sys
from .objects.nutrient_dict import nutrient_dict, index_from_name

def report(meal):
    report = []
    _nutrient_dict = nutrient_dict()()
    for i in range(0, len(meal.nutrients)):
        name = meal.nutrients[i]["name"]
        rda = _nutrient_dict[i]["rda"]
        limit = _nutrient_dict[i]["limit"]
        value = meal.nutrients[i]["value"]
        unit = meal.nutrients[i]["unit"]
        state = ""
        if rda == None:
            rda = 0
        if limit == None:
            limit = sys.maxsize
        if value < rda:
            state = "deficient"
        elif value > limit:
            state = "excessive"
        else:
            state = "satisfactory"
        if limit == sys.maxsize:
            limit = None
        report.append({"name":name, "rda":rda, "limit":limit, "value":value, "state":state, "unit":unit})
    return report

def export_report(meal, path):
    with open(path, "w",newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        # Write profile information
        writer.writerow(['TDEE',None,tdee])
        writer.writerow(['Carb Ratio',carb_p,carb_p*tdee])
        writer.writerow(['Protein Ratio',protein_p,protein_p*tdee])
        writer.writerow(['Fat Ratio',fat_p,fat_p*tdee])
        writer.writerow([''])
        # Write nutritional information
        writer.writerow(['Nutrient', 'RDA', 'Limit'])
        for i in range(0, len(meal.nutrients)):
            name = meal.nutrients[i]["name"]
            row = [name]
            if nutrient_dict[i]["rda"] == None:
                row.append("None")
            else:
                row.append(nutrient_dict[i]["rda"])
            if nutrient_dict[i]["limit"] == None:
                row.append("None")
            else:
                row.append(nutrient_dict[i]["limit"])
            row.append(meal.nutrients[i]["value"])
            i += 1
            writer.writerow(row)
