import pandas as pd
from Item import Item
from Item import ItemEncoder
import json
from pathlib import Path
from IkeaManager import IkeaManager
import os



Ikea = IkeaManager()
df = Ikea.prepare_df()


number_dict = {}

for index, row in df.iterrows():
    if "." in row["comment"]:
        number_dict[row["comment"]] = row["ikea_id"]

with open("numbers.json", "w") as f:
    json.dump(number_dict, f)

