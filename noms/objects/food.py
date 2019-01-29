import copy

class Food:
    def __init__(self, _dict):
        self.desc = _dict["food"]["desc"]
        self.nutrients = _dict["food"]["nutrients"]
    def __add__(self, other):
        assert len(self.nutrients) == len(other.nutrients)
        return_copy = copy.deepcopy(self)
        self_tracked = [i["nutrient_id"] for i in self.nutrients]
        other_tracked = [i["nutrient_id"] for i in other.nutrients]
        tracked_nutrients = list(set(self_tracked)|set(other_tracked))
        i = 0
        for id in tracked_nutrients:
            return_copy.nutrients[i]["value"] = round(other.nutrients[i]["value"]+return_copy.nutrients[i]["value"],2)
            i += 1
        return return_copy