import requests
import json

class Client:
    url = 'https://api.nal.usda.gov/usda/ndb'

    def __init__(self, key):
        '''
        A Client instance must be initialized with a key from
        data.gov. This is free to obtain, and you can request one
        here: https://api.data.gov/signup/
        '''
        self.key = key

    def call(self, params, url_suffix):
        ''' target_url could be:
        https://api.nal.usda.gov/usda/ndb/V2/reports
        https://api.nal.usda.gov/usda/ndb/search
        depending on which service of the api is being used
        '''
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
        return self.call(params, '/search')
    
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