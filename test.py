import noms
import copy

def _client():
    key = open("key.txt", "r").read()
    client = noms.Client(key)
    assert type(client) == noms.Client
    assert client.key == key
    return client

def _search():
    client = _client()
    broc_search = client.search_query("Raw Broccoli")
    assert "items" in broc_search.json.keys()
    assert len(broc_search.json["items"]) > 5
    uni_search = client.search_query("Unicorn meat")
    assert uni_search.json == None

def _foods():
    client = _client()
    food_list = client.get_foods({
        '173410':20, # 01001':20,
        '1100335':100, #'01132':100,
        '1103883': 80, #'09037':80,
        '175167':150, #15076':150,
        '1102597':140, #'09201':140,
        '1104292':300, #'14278':300,
        '1100612':20, #'12006':20,
        '1101628':150,#'20041':150,
        '1100429':50, #'16057':50,
        '1103116':50, #'11233':50,
        '1104032':10,#'19904':10,
        '1104331':1000 #14400':1000 # literally an entire liter of coke
    })
    assert len(food_list) == 12
    assert type(food_list[0]) == noms.Food
    assert type(food_list[0].desc) == type('')

def _meal():
    client = _client()
    food_list = client.get_foods({
        '173410':20, # 01001':20,
        '1100335':100, #'01132':100,
        '1103883': 80, #'09037':80,
        '175167':150, #15076':150,
        '1102597':140, #'09201':140,
        '1104292':300, #'14278':300,
        '1100612':20, #'12006':20,
        '1101628':150,#'20041':150,
        '1100429':50, #'16057':50,
        '1103116':50, #'11233':50,
        '1104032':10,#'19904':10,
        '1104331':1000 #14400':1000 # literally an entire liter of coke
    })
    meal = noms.Meal(food_list)
    assert type(meal) == noms.Meal
    assert len(meal.foods) == 12
    return meal

def _report(meal):
    r = noms.report(meal)
    assert len(r) == len(noms.nutrient_dict()())

def _sort(meal):
    m = copy.deepcopy(meal)
    m.sort_by_top("Sugar")
    assert m.foods[0].data['fdcId'] == 1104331 # the most sugar-dense food in the meal is coke

def _pantry():
    client = _client()
    pantry_items = {
        "1097517":100, # 2% milk
        "1097878":100, # cocoa powder
        "1100383":100, # lima beans
        "1100549":100, # pistachio
        "1100918":100, # ice cream
        "1102594":100, # lemon
        "1102710":100, # strawberries
        "1102880":100, # baked potato
        "1103193":100, # raw carrots
        "1103261":100, # baked sweet potato
        "1103645":100, # peas
        "1103845":100, # garlic
        "1103861":100, # olive oil
        "1103883":100, # avocado
        "1104493":100, # bottled water
        "1105430":100, # red delicious apple
        "168436":100, # shiitake mushrooms
        "168917":100, # quinoa, cooked
        "171890":100, # coffee brewed with tap water
        "173410":100, # butter, salted
        "173423":100, # fried egg
        "173430":100, # butter, without salt
        "174608":100, # chicken breast oven-roasted
        "1097512":100, # milk, whole
        "1097521":100, # skim milk
        "1099608":100, # steak
        "1099796":100, # hamburger
        "1099888":100, # turkey
        "1100335":100, # scrambled eggs
        "1100393":100, # pinto beans
        "1100410":100, # black beans
        "1100429":100, # chickpeas
        "1100555":100, # almond
        "1100612":100, # chia
        "1101112":100, # pizza
        "1101628":100, # brown rice cooked
        "1102597":100, # oranges
        "1102702":100, # blueberry
        "1102708":100, # raspberry
        "1103116":100, # kale
        "1103136":100, # spinach, raw
        "1103183":100, # broccoli
        "1103358":100, # lettuce
        "1103860":100, # flaxseed
        "1104032":100, # dark chocolate
        "1104292":100, # brewed green tea
        "1104331":100, # coke
        "1104492":100, # tap water
        "168880":100, # white rice enriched cooked
        "170050":100, # tomato, red, cooked
        "170285":100, # pearled barley
        "171354":100, # orange juice
        "171370":100, # pretzel
        "173424":100, # hard boiled eggs
        "173945":100, # banana
        "174993":100, # donut
        "175167":100, # atlantic salmon
        "324860":100 # peanut butter smooth
        }
    pantry_food = client.get_foods(pantry_items)
    #import pickle
    #pantry_food =pickle.load(open('pantry_foods_data.pkl', 'rb')) 
    pantry = noms.Meal(pantry_food)
    assert type(pantry) == noms.Meal
    assert pantry.nutrients[0]["name"] == noms.nutrient_dict()()[0]["name"]
    return pantry

def _gen_recommendations(meal, pantry, verbose=False):
    recommendations = noms.generate_recommendations(meal, pantry, noms.nutrient_dict, 3, verbose)
    pre_meal_loss = noms.analyze.loss(meal, noms.nutrient_dict)
    post_meal = noms.Meal(meal.foods + [pantry[recommendations[0][1]]])
    post_meal_loss = noms.analyze.loss(post_meal, noms.nutrient_dict)
    # check that the loss of the new meal is lower
    assert post_meal_loss < pre_meal_loss

def _remove_recommendation(meal):
    result = noms.recommend_removal(meal, noms.nutrient_dict)
    # check that we are recommending the user not to have a liter of coke
    #assert meal.foods[result].desc["ndbno"] == "14400"
    assert meal.foods[result].data['fdcId'] == 1104331

def test():
    print('testing noms.client .....')
    _client()
    print('testing search ......')
    _search()
    print('testing a list of foods .....')
    _foods()
    print('testing meal object ....')
    meal = _meal()
    #import pickle
    #meal = pickle.load(open('mytestmeal.pkl', 'rb'))
    print('testing reporting .....')
    _report(meal)
    print('testing sorting .....')
    _sort(meal)
    print('creating pantry .....')
    pantry = _pantry()
    print('generating recommendation .....')
    _gen_recommendations(meal, pantry.foods)
    print('removing recommendation ......')
    _remove_recommendation(meal)

if __name__ == "__main__":
    test()
