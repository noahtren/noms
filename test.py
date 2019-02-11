def _test():
    # Test Client
    from noms.client.main import Client
    key = open("key.txt","r").read()
    client = Client(key)

    # Test Imports
    from noms.objects.food import Food, Meal
    from noms.search import get_results, print_results
    from noms.food import foods
    from noms.report import export_report, report

    # Test Search
    print_results(get_results("Raw Broccoli", client))
    print_results(get_results("Cola", client))

    # Test Food
    food_list = foods({'11090':100, '14400':100}, client)
    m = Meal(food_list)

    # Test Report
    r = report(m)
    for i in r:
        print(i)
    export_report(m, "report.csv")

    # Test Sorting
    from noms.objects.nutrient_dict import index_from_name
    m.sort_by_top("Sugar")
    ni = index_from_name("Sugar")
    for food in m.foods:
        print(food.nutrients[ni])
    
    # Test Long Call
    pantry = {
    # DAIRY AND EGG
    "01001":100, # butter, salted
    "01145":100, # butter, without salt
    "01079":100, # 2% milk
    "01077":100, # milk, whole
    "01086":100, # skim milk
    "01132":100, # scrambled eggs
    "01129":100, # hard boiled eggs
    "01128":100, # fried egg
    # MEAT
    "15076":100, # atlantic salmon
    "07935":100, # chicken breast oven-roasted
    "13647":100, # steak
    "05192":100, # turkey
    # FRUIT
    "09037":100, # avocado
    "09316":100, # strawberries
    "09050":100, # blueberry
    "09302":100, # raspberry
    "09500":100, # red delicious apple
    "09040":100, # banana
    "09150":100, # lemon
    "09201":100, # oranges
    "09132":100, # grapes
    # PROCESSED
    "21250":100, # hamburger, 6 oz
    "21272":100, # pizza (2 slices)
    "19088":100, # ice cream
    "19057":100, # doritos (25)
    "18249":100, # donut
    # DRINK
    "14400":100, # coke
    "14429":100, # tap water
    "14433":100, # aquafina bottled water
    "09206":100, # orange juice
    "14278":100, # brewed green tea
    "14209":100, # coffee brewed with tap water
    # (milk is included in dairy group)
    # GRAIN
    "12006":100, # chia
    "12220":100, # flaxseed
    "20137":100, # quinoa, cooked
    "20006":100, # pearled barley
    "20051":100, # white rice enriched cooked
    "20041":100, # brown rice cooked
    "12151":100, # pistachio
    "19047":100, # pretzel
    "12061":100, # almond
    # LEGUME
    "16057":100, # chickpeas
    "16015":100, # black beans
    "16043":100, # pinto beans
    "16072":100, # lima beans
    "16167":100, # peanut butter smooth
    # VEGETABLE
    "11124":100, # raw carrots
    "11090":100, # broccoli
    "11457":100, # spinach, raw
    "11357":100, # baked potato
    "11508":100, # baked sweet potato
    "11530":100, # tomato, red, cooked
    "11253":100, # lettuce
    "11233":100, # kale
    "11313":100, # peas
    "11215":100, # garlic
    # OTHER
    "04053":100, # olive oil
    "19904":100, # dark chocolate
    "14058":100, # protein powder isolate
    "11238":100, # shiitake mushrooms
    "19165":100, # cocoa powder
    }
    pantry_food = foods(pantry, client)
    P = Meal(pantry_food)
    for f in P.foods:
        print(f.desc["name"])

if __name__ == "__main__":
    _test()