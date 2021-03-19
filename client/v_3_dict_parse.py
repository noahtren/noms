import operator
from ..objects.food import Food

def search_parse(search_results):
    """ Return a simplified version of the json object returned from the USDA API.
    This deletes extraneous pieces of information that are not important for providing
    context on the search results.
    """
    if 'errors' in search_results.keys():
        return None
    # Store the search term that was used to produce these results
    search_term = search_results['foodSearchCriteria']['query']
    if search_results['foods'] == []:
        return None
    else:
        return dict(search_term=search_term, items=search_results['foods'])

def food_parse(food_results, nutrient_dict, values):
    """ Return a simplified version of the json object returned from the USDA API.
    This deletes extraneous pieces of information, including nutrients that are
    not tracked. It also exchanges nutrient names for their more common names, or "nicknames",
    as defined in noms.objects.nutrient_dict
    """
    if len(food_results) == 0:
        return None
    food_arr = []
    tracked_nutrients = []
    nutrient_nicknames = []
    for nutrient in nutrient_dict:
        if "nickname" in nutrient.keys():
            nutrient_nicknames.append(nutrient["nickname"])

        else:
            nutrient_nicknames.append(None)
        nutrient['nutrient_id'] = str(nutrient['nutrient_id'])
        tracked_nutrients.append(nutrient["nutrient_id"])
    # Remove extraneous pieces of data in the food description
    to_del = {'food':["sr", "type", "sources", "footnotes", "langual"], 
              'desc':["sd", "sn", "cn", "manu", "nf", "cf", "ff", "pf", "r", "rd", "ru", "ds"],
              # This current implementation deletes the measurement data from the database,
              # this could be changed later to provide richer data and easy UX tools (select measure)
              'nutrients':["derivation", "sourcecode", "dp", "se"]}
    # Iterate through each food and remove extra information, and simplify names
    f = 0
    for food in food_results:
        # create a 'value' key and equate it to 'amount'
        # to take into account the changes in the new
        # api results
        for nutrient in food["foodNutrients"]:
            if 'amount' in nutrient.keys():
                nutrient['value'] = nutrient['amount']
            else:
                nutrient['value'] = 0
            nutrient['name'] = nutrient['nutrient']['name']
            nutrient['unit'] = nutrient['nutrient']['unitName']
        #for del_item in to_del["food"]:
        #    del food["food"][del_item]
        #for del_item in to_del["desc"]:
        #    del food["food"]["desc"][del_item]

        # sort nutrients by id if not already
        n_list = food["foodNutrients"]
        n_list.sort(key=lambda x: x['nutrient']['number'])
        # end sort
        n = 0
        for nutrient in food["foodNutrients"]:
            if n == len(tracked_nutrients):
                break
            # check if this is a nutrient we should record
            if (nutrient["nutrient"]['number']) == (tracked_nutrients[n]):
                potential_name = nutrient_nicknames[n]
                if potential_name != None:
                    nutrient["nutrient"]["name"] = potential_name
                #for del_item in to_del["nutrients"]:
                #    del nutrient[del_item]
                n += 1

            # check if the food doesn't contain a tracked nutrient
            while n < len(tracked_nutrients) and (nutrient["nutrient"]["number"]) > tracked_nutrients[n]:
                to_insert = nutrient_dict[n]
                to_insert.update(value=0)
                to_insert["nutrient"] = {"number":to_insert["nutrient_id"]}
                food["foodNutrients"].insert(n,to_insert)
                n += 1
        while n < len(tracked_nutrients) and food["foodNutrients"][-1]["nutrient"]["number"] < tracked_nutrients[-1]:
            to_insert = nutrient_dict[n]
            to_insert.update(value=0)

            to_insert["nutrient"] = {"number":to_insert["nutrient_id"]}
            food["foodNutrients"].insert(n,to_insert)
            n += 1
        n = 0
        n_to_del = []
        for nutrient in food["foodNutrients"]:
            # check if this is a nutrient we should delete
            #if nutrient["nutrient_id"] not in tracked_nutrients:
            if (nutrient["nutrient"]["number"]) not in tracked_nutrients:
                n_to_del.append(n)
            n += 1
        offset = 0
        for del_n in n_to_del:
            del food["foodNutrients"][del_n - offset]
            offset += 1
        # sort nutrients by id if not already
        n_list = food["foodNutrients"]
        n_list.sort(key=lambda x: x['nutrient']['number'])
        # end sort
        n = 0
        for nutrient in food["foodNutrients"]:
            if nutrient_nicknames[n] != None:
                nutrient["name"] = nutrient_nicknames[n]
            nutrient["value"] = nutrient["value"] * (values[f]/100)
            n += 1
        f += 1
        food_arr.append(Food(food))
    return food_arr
