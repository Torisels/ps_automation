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

df = df.loc[61:175]
print(df)


items = []
counter = 1
print(f"Analyzing {Ikea.COLLECTION_NAME}")
print("Photos that are missing: ")
for index, row in df.iterrows():
    items.append([Item(number=index,  **row.to_dict())])
    p = Ikea.INPUT_PHOTOS_PATH / Path(items[-1][0].file_name)
    n = row["name"]
    if type(n) != str:
        n = ""
    if not p.exists():
        print(
            f"{counter:2}. ORIGIN: {row['HUB']} || PE(filename): {items[-1][0].file_name:15} || NAME: {n:10} || ART no: {row['ART no']:12} || "
            f"STATUS: {row['status']} ")
        counter +=1