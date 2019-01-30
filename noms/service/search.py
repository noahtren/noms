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
    for item in search_obj["items"]:
        if len(item["name"]) > 68:
            item["name"] = item["name"][:68] + ".."
        if len(item["group"]) > 23:
            item["group"] = item["group"][:23] + ".."
        print("{name:<70} {group:^25} {id:>15}".format(name=item["name"],group=item["group"],id=item["ndbno"]))
    print("="*112)