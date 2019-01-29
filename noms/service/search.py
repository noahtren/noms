from ..client.main import Client
from ..client.dict_parse import search_parse
import operator

def search(query, client, max_entries=None):
    search_obj = client.search_query(query)
    search_obj = search_parse(search_obj)
    print("==========")
    print("Search for {}".format(search_obj["search_term"]))
    if max_entries == None:
        max_entries = len(search_obj["items"])
    if max_entries < len(search_obj["items"]):
        search_obj["items"] = search_obj["items"][:max_entries]
    search_obj["items"].sort(key=operator.itemgetter("group"))
    for item in search_obj["items"]:
        print("{} Group: {} Id: {}".format(item["name"],item["group"],item["ndbno"]))
    print("==========")