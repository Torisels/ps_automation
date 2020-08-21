import pandas as pd
from Item import Item
from Item import ItemEncoder
import json
from pathlib import Path
from IkeaManager import IkeaManager
Ikea = IkeaManager()
df = Ikea.prepare_df()

count_frame = df.groupby("name").count()
count_frame = count_frame["Placement"].to_dict()

print(df)


items = []
counter = 1
print(f"Analyzing {Ikea.COLLECTION_NAME}")
for index, row in df.iterrows():
    p = Ikea.INPUT_PHOTOS_PATH / Path(Item.get_file_name(**row.to_dict()))
    n = row["name"]
    if type(n) != str:
        n = ""
    if not p.exists():
        print(
            f"{counter:2}. ORIGIN: {row['HUB']} || PE(filename): {Item.get_file_name(**row.to_dict()).lstrip():15} || NAME: {n:10} || ART no: {str(row['ART no']).ljust(12)} || "
            f"STATUS: {row['status']} ")
        counter +=1