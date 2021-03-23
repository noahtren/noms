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
    # nutrient_dict is a global variable; some of the 
    # assignments below alters it value across modules
    # thus making a shallow copy it
    nutrient_dict = nutrient_dict()()
    for nutrient in nutrient_dict:
        if "nickname" in nutrient.keys():
            nutrient_nicknames.append(nutrient["nickname"])

        else:
            nutrient_nicknames.append(None)
        #nutrient['nutrient_id'] = str(nutrient['nutrient_id'])
        tracked_nutrients.append(nutrient["nutrient_id"])
    # Iterate through each food and simplify names
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
            nutrient['nutrient']['number'] = float(nutrient['nutrient']['number'])
            nutrient['name'] = nutrient['nutrient']['name']
            nutrient['unit'] = nutrient['nutrient']['unitName']
            nutrient['nutrient_id'] = nutrient['nutrient']['number']

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
                n += 1

            # check if the food doesn't contain a tracked nutrient
            while n < len(tracked_nutrients) and (nutrient["nutrient"]["number"]) > tracked_nutrients[n]:
                to_insert = nutrient_dict[n].copy()
                to_insert.update(value=0)
                to_insert["nutrient"] = {"number":to_insert["nutrient_id"]}
                food["foodNutrients"].insert(n,to_insert)
                n += 1
        while n < len(tracked_nutrients) and food["foodNutrients"][-1]["nutrient"]["number"] < tracked_nutrients[-1]:
            to_insert = nutrient_dict[n].copy()
            to_insert.update(value=0)

            to_insert["nutrient"] = {"number":to_insert["nutrient_id"]}
            food["foodNutrients"].insert(n,to_insert)
            n += 1
        n = 0
        n_to_del = []
        for nutrient in food["foodNutrients"]:
            # check if this is a nutrient we should delete
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
        # deleting keys except that in keys_to_keep
        keys_to_keep = ['nutrient_id', 'name', 'group', 'unit', 'value']
        for nutrient in food['foodNutrients']:
            nutrient_copy = nutrient.copy()
            for key in nutrient_copy:
                if key  not in keys_to_keep:
                    del nutrient[key]

        f += 1
        food_arr.append(Food(food))
    return food_arr
