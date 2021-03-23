from ..client.main import Client
from ..client.dict_parse import search_parse
import operator

def get_results(query, client):
    search_obj = client.search_query(query)
    search_obj = search_parse(search_obj)
    return search_obj

def print_results(search_obj, max_entries=None):
    print("="*112)
    print("Search results for \'{}\' on USDA Standard Reference Database".format(search_obj["search_term"]))
    print("="*112)
    if max_entries == None:
        max_entries = len(search_obj["items"])
    if max_entries < len(search_obj["items"]):
        search_obj["items"] = search_obj["items"][:max_entries]
    search_obj["items"].sort(key=operator.itemgetter("group"))
    print("{name:<72} {group:^30} {id:>8}".format(name="Name",group="Group",id="ID"))
    for item in search_obj["items"]:
        if len(item["name"]) > 70:
            item["name"] = item["name"][:70] + ".."
        if len(item["group"]) > 28:
            item["group"] = item["group"][:28] + ".."
        print("{name:<72} {group:^30} {id:>8}".format(name=item["name"],group=item["group"],id=item["ndbno"]))
    print("="*112)