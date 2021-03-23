from scipy.optimize import minimize
from .objects.food import Food, Meal
import copy 
import sys
import os

def norm_rda_deficit(norm_rda_arr):
    """ Returns a modified list of nutrient dicts in which value represents 
    a fraction of how much a given nutrient has been satisfied. A value of
    0 represents full satisfaction, and 1 represents no satisfaction. """
    r_nut = copy.deepcopy(norm_rda_arr)
    for ni, _ in enumerate(r_nut):
        r_nut[ni]['value'] = 1 - r_nut[ni]['value']
    return r_nut

def loss(meal, nutrient_dict, verbose=False):
    if verbose:
        print("Deficit breakdown of meal:")
    deficit = norm_rda_deficit(meal.norm_rda(nutrient_dict))
    loss = 0; ni = 0
    for nut in deficit:
        if verbose:
            print("{nut:<20}: {val:>10} percent unmet".format(nut=nut['name'], val=round(nut['value'] * 100, 1)))
        loss += nut['value'] ** 2
        ni += 1
    return loss

def assess_deficit(meal, nutrient_dict):
    print("Deficit breakdown of meal:")
    deficit = norm_rda_deficit(meal.norm_rda(nutrient_dict))
    loss = 0; ni = 0
    for nut in deficit:
        #if nut['value'] != 0:
        print("{nut:<20}: {val:>10} percent unmet".format(nut=nut['name'], val=round(nut['value'] * 100, 1)))
        loss += nut['value'] ** 2
        ni += 1
    print("Loss: ", round(loss, 2))

def best_contributors(k, meal, suggestion, nutrient_dict, x):
    """
    Returns the top nutrients that are being satisfied by a give suggestion
    """
    sug_norm = suggestion.norm_rda(nutrient_dict)
    sug_norm = copy.deepcopy(sug_norm)
    nutrient_residuals = []
    req = norm_rda_deficit(meal.norm_rda(nutrient_dict))
    ni = 0
    for nut in sug_norm:
        nut['value'] *= k
        this_nutrient_required = req[ni]['value']
        if this_nutrient_required > 0:
            resid = abs((this_nutrient_required ** 2) - ((nut['value']-this_nutrient_required) ** 2))
            nutrient_residuals.append(dict(value=resid, name=nut['name']))
        ni += 1
    return sorted(nutrient_residuals, key=lambda x: x['value'], reverse=True)[:x]

def suggestion_loss(meal, suggestion, nutrient_dict):
    """
    Minimizes the squared residual of each normed nutrient for a given
    food suggestion and meal. These minimized values are then used to
    find the best food recommendation for a given meal in the context
    of a nutrient_dict
    """
    def scaled_loss(k, *args):
        _nutrient_dict = nutrient_dict()()
        sug_norm = args[1].norm_rda(args[2])
        sug_norm = copy.deepcopy(sug_norm)
        loss = 0; ni = 0
        for nut in sug_norm:
            nut['value'] *= k
            this_nutrient_required = args[0][ni]['value']
            # don't track it as loss if it's superfluous
            # i.e. its not required but there is no limit
            if not (this_nutrient_required == 0 and _nutrient_dict[ni]['limit'] == None):
                '''if 'nickname' in nutrient_dict[ni].keys() and nutrient_dict[ni]['nickname'] == "Sugar":
                    loss += ((nut['value'] - this_nutrient_required) ** 2) * 3
                elif not nutrient_dict[ni]['group'] == "Proximates":
                    loss += (nut['value'] - this_nutrient_required) ** 2'''
                #if not (nutrient_dict[ni]['name'] == "Sugars, total"):
                loss += (nut['value'] - this_nutrient_required) ** 2
            ni += 1
        return loss
    _nutrient_dict = nutrient_dict()()
    required_normed_nutrients = norm_rda_deficit(meal.norm_rda(_nutrient_dict))
    sol = minimize(scaled_loss, 1, args=(required_normed_nutrients, suggestion, _nutrient_dict), bounds=[(0.05, sys.maxsize)], tol=1e-2)
    """
    # this can be uncommented to display a graph showing the convergence to minimize loss
    # as the mass of the given food is scaled
    import matplotlib.pyplot as plt
    xs = []; losses = []
    for x in range(0, 20):
        inp = sol.x[0] * (x/10)
        xs.append(inp)
        losses.append(scaled_loss(inp, required_normed_nutrients, suggestion, nutrient_dict))
    plt.plot(xs, losses)
    plt.show()
    """
    return (scaled_loss(sol.x[0], required_normed_nutrients, suggestion, _nutrient_dict), sol.x[0])

def generate_recommendations(meal, pantry, nutrient_dict, n, verbose=False):
    """
    Gives the top n food recommendations to satisfy daily nutrition in
    context of the current foods, available foods, and a nutrient_dict full
    of RDAs.
        Meal is a meal object representing the current day's meal
        Pantry is an array of Food objects representing potential foods
        (Note: pantry food objects must have a mass of 100g)
        Nutrient Dict is a personalized list of rdas and limits based on the user's preference
    """
    rec_data = []
    rec_index = 0; rec_loss = sys.maxsize; rec_optimum = 0
    for rec_i, _ in enumerate(pantry):
        sug_obj = suggestion_loss(meal, pantry[rec_i], nutrient_dict)
        cur_loss = sug_obj[0]
        # print("name:", pantry[rec_i].desc['name'], "loss:", sug_obj[0], "k:", sug_obj[1])
        if cur_loss < rec_loss:
            rec_loss = cur_loss
            rec_index = rec_i
            rec_optimum = sug_obj[1]
        rec_data.append([copy.copy(cur_loss), copy.copy(rec_i), copy.deepcopy(sug_obj[1])])
        if verbose:
            print(pantry[rec_i].desc['name'], cur_loss)
            print("^" * 50)
    rec_data.sort(key=lambda x: x[0])
    return rec_data[:n]

def recommend_removal(meal, nutrient_dict):
    assert type(meal) == Meal
    o_loss = loss(meal, nutrient_dict) # calculate the original loss
    losses = []
    for i in range(0, len(meal.foods)):
        # compute the loss for the meal without each food
        this_meal = Meal([food for j, food in enumerate(meal.foods) if j != i])
        losses.append(loss(this_meal, nutrient_dict))
    if min(losses) < o_loss:
        return losses.index(min(losses)) # removing a certain food is beneficial
    else:
        return -1 # removing any certain food is detrimental
