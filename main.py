import csv
from Item import Item
import json
from json import JSONEncoder
from pathlib import Path
from collections import Counter
import re

scales = {1: [70], 2: [38, 45], 3: [40, 40, 45]}
OUTPUT_PATH = Path("E:/Ikea_Projekt/input.json")
INPUT_PHOTOS_PATH = Path("E:/Ikea_Projekt/input_photos")


class EmployeeEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


regex = re.compile(r"((\d{1,3})x(\d{1,3}))\s")

with open('data4.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    different_pic_count = 0
    csv_reader = list(csv_reader)
    items = [[]]
    current_name = csv_reader[0]["Name"]
    not_exists_counter = 0

    for row in csv_reader:
        if row["ART no"] == "":
            continue
        desc1 = row["Product type"]
        desc3 = row["Short product description (like: colour, material: wood, plastic, metal, any additional " \
                    "necessary information"].split(" ")
        desc1 += " " + desc3[0] + " cm"
        matches = regex.finditer(desc1, re.MULTILINE)
        g = [m.groups() for m in matches]
        g = g[0]

        desc2 = row["MATERIAL"]
        desc3 = " ".join(desc3[1:])
        desc = desc1 + "\r" + desc2 + "\r" + desc3

        input_filename = row["status"] + ".jpg"
        p = INPUT_PHOTOS_PATH / Path(input_filename)
        if not p.exists():
            print(
                f"Photo with filename-name-placement: {input_filename}-{row['Name']}-{row['Placement']} does not exist in the input folder!")
            not_exists_counter += 1

        more_options = row["Comment -Add - MORE OPTIONS AVAILABLE or 3rd size"]
        if more_options == "MORE OPTIONS AVAIABLE ":
            more_options = True
        else:
            more_options = False

        item = Item((row["Placement"]).zfill(2), input_filename, row["Name"], desc, row["Art. / SPR number"],
                    row["(DE) EUR"], row["(US) USD"], row["(CN) CNY"], int(g[1]), int(g[2]), more_options, 55)

        if row["Name"] != current_name:
            current_name = row["Name"]
            different_pic_count += 1
            items.append([])

        items[different_pic_count].append(item)

for item in items:
    if len(item) > 1:
        item.sort(key=lambda i: i.height)
        if len(item) == 2:
            item[1].scale = scales[2][1]
            item[0].scale = item[1].scale * item[0].height / item[1].height
        else:
            item[2].scale = scales[3][2]
            item[1].scale = item[2].scale * item[1].height / item[2].height
            item[0].scale = item[2].scale * item[0].height / item[2].height

    else:
        item[0].scale = scales[len(item)][0]

with OUTPUT_PATH.open("w") as f:
    json.dump(items, f, cls=EmployeeEncoder)

different_versions_counter = Counter()

for item in items:
    different_versions_counter[len(item)] += 1

print("\n========================================")
print("STATISTICS: ")
print(f"Number of psd projects: {len(items)}")
print(f"Number of lacking photos: {not_exists_counter}")
print("========================================")
for type_, count in different_versions_counter.items():
    print(f"{type_}-photo psd projects: {count}")
print("========================================")
