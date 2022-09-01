import json
import os

if __name__ == "__main__":

    with open("template_data/data_base.json") as file:
        src = json.load(file)

    islam_counter = 0

    for item in src:
        if item.get("Religion") in ["Unknown", "Islam"]:
            islam_counter += 1

    





