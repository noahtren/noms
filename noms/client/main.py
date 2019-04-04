import requests
import json
import operator
from .dict_parse import search_parse

class SearchResults():
    def __init__(self, json):
        self.json = json
    def __str__(self, max_entries=None):
        r_str = ""
        if self.json == None:
            r_str += "There are no search results for this query\n"
        else:
            r_str +="="*112 + "\n"
            r_str +="Search results for \'{}\' on USDA Standard Reference Database".format(self.json["search_term"]) + "\n"
            r_str +="="*112 + "\n"
            if max_entries == None:
                max_entries = len(self.json["items"])
            if max_entries < len(self.json["items"]):
                self.json["items"] = self.json["items"][:max_entries]
            self.json["items"].sort(key=operator.itemgetter("group"))
            r_str +="{name:<72} {group:^30} {id:>8}".format(name="Name",group="Group",id="ID") + "\n"
            for item in self.json["items"]:
                if len(item["name"]) > 70:
                    item["name"] = item["name"][:70] + ".."
                if len(item["group"]) > 28:
                    item["group"] = item["group"][:28] + ".."
                r_str +="{name:<72} {group:^30} {id:>8}".format(name=item["name"],group=item["group"],id=item["ndbno"]) + "\n"
            r_str +="="*112 + "\n"
        return r_str

class Client:
    url = 'https://api.nal.usda.gov/usda/ndb'

    def __init__(self, key):
        """
        A Client instance must be initialized with a key from
        data.gov. This is free to obtain, and you can request one
        here: https://api.data.gov/signup/
        """
        self.key = key

    def call(self, params, url_suffix):
        """ target_url could be:
        https://api.nal.usda.gov/usda/ndb/V2/reports
        https://api.nal.usda.gov/usda/ndb/search
        depending on which service of the api is being used
        """
        target_url = self.url + url_suffix 
        # add the key to the API call
        call_params = dict(params, api_key=self.key)
        response = json.loads(requests.get(url=target_url, params=call_params).text)
        return response

    def search_query(self, name):
        params = dict(
            q=name,
            ds='Standard Reference',
            format='json'
        )
        return SearchResults(search_parse(self.call(params, '/search')))
    
    def food_query(self, ids):
        # allow for either a single id (ndbno) query, or a list of queries
        if type(ids) == list:
            if len(ids) > 25:
                raise Exception("Too many Food ID arguments. API limits it to 25.")
        params = dict(ndbno=ids)
        params.update(dict(type='f', format='json'))
        return_obj = self.call(params, '/V2/reports')
        offset = 0
        if 'foods' not in return_obj:
            print("See the following error: {}".format(return_obj))
            exit()
        for i in range(0, len(return_obj["foods"])):
            if 'error' in return_obj["foods"][i-offset].keys():
                del return_obj["foods"][i-offset]
                offset += 1
        return return_obj
    
