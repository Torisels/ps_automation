import pandas as pd
from Item import Item
from Item import ItemEncoder
import json

EXCEL_PATH = r"E:\Ikea_Projekt\input_excel\WORKING FILE_ Rugs and doormats plus CN.xlsx"
RENAMING_DICT = {"NAME": "name", "How to order": "badge_type", "Product type": "description_1",
                 "MATERIAL": "description_2",
                 "Short product description (like: colour, material: wood, plastic, metal, any additional necessary information": "description_3",
                 "Art. / SPR number": "ikea_id", "(DE) EUR": "eur", "(US) USD": "usd", "(CN) CNY": "cny",
                 "PE": "product_id"}

COLUMNS_TO_EXCLUDE = [i for i in range(15, 31)]

df = pd.read_excel(EXCEL_PATH)

df.drop(columns=["HUB", "PA", "\"colorswatch\"", "status", "ART no", "Packshot type"], inplace=True)
df.drop(df.columns[list(df.columns).index("comment") + 1:], axis=1, inplace=True)

df.rename(columns=RENAMING_DICT, inplace=True)

count_frame = df.groupby("name").count()
count_frame = count_frame["Placement"]

data = df.loc[64:, :]
items = []

for index, row in data.iterrows():
    items.append([Item(number=index, **row.to_dict())])


with open("result.json", "w") as f:
    json.dump(items, f, cls=ItemEncoder)

print(items)