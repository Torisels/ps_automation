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

data = df.loc[139:175]
print(data)

items = [[] for _ in range(len(data))]

dp_index = 0

for index, row in data.iterrows():
    item = Item(number=index, **row.to_dict())
    p = Ikea.INPUT_PHOTOS_PATH / Path(item.file_name)
    if not p.exists():
        print(f"Missing: {item.file_name}")
        continue

    # try:
    #     if items[dp_index][0].name != item.name:
    #         dp_index += 1
    # except IndexError:
    #     pass

    items[dp_index].append(item)

    # if row["name"] in count_frame and count_frame[row["name"]] > 1:
    #     a = 1
    # else:
    dp_index += 1

double_product_count = 0
triple_product_count = 0

print("================================================================")
for item in items[::-1]:
    if len(item) == 0:
        items.pop()
    if len(item) == 2:
        double_product_count += 1
        print(f"{double_product_count}. Double product: {item[0].name}")
print("================================================================")

print(f"Different items count: {len(items)}")

with open("result.json", "w") as f:
    json.dump(items, f, cls=ItemEncoder)
