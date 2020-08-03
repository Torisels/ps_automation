import csv
from Item import Item
import json
from json import JSONEncoder
from pathlib import Path
from collections import Counter

OUTPUT_PATH = Path("E:/Ikea_Projekt/input.json")
INPUT_PHOTOS_PATH = Path("E:/Ikea_Projekt/input_photos")


class EmployeeEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


with open('input.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    different_pic_count = 0
    csv_reader = list(csv_reader)
    items = [[]]
    current_name = csv_reader[0]["Name"]
    not_exists_counter = 0

    for row in csv_reader:
        if row["ART no"] == "":
            continue
        desc1 = row["desc1"]
        desc2 = row["desc2"].split(" ")
        desc1 += " " + desc2[0] + " cm"
        desc2 = " ".join(desc2[1:])
        desc = desc1 + "\r" + desc2

        input_filename = row["status"] + ".jpg"
        p = INPUT_PHOTOS_PATH / Path(input_filename)
        if not p.exists():
            print(f"Photo with filename-name-placement: {input_filename}-{row['Name']}-{row['Placement']} does not exist in the input folder!")
            not_exists_counter += 1

        item = Item(row["Placement"], input_filename, row["Name"], desc, row["Art. / SPR number"],
                    row["(DE) EUR"], row["(US) USD"], row["(CN) CNY"])

        if row["Name"] != current_name:
            current_name = row["Name"]
            different_pic_count += 1
            items.append([])

        items[different_pic_count].append(item)

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
