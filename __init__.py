name = "noms"
__version__ = "0.1.7"
__version_info__ = tuple(int(i) for i in __version__.split('.'))

# client object
from noms.client.main import Client
# food and meal objects
from noms.objects.food import Food, Meal
# csv reports
from noms.report import export_report, report

# nutrient dict
from noms.objects.nutrient_dict import index_from_name
from noms.objects.nutrient_dict import nutrient_dict

# recommendation method
from noms.analyze import generate_recommendations
from noms.analyze import recommend_removal
