DIR_PATH = r"E:\IKEA_ALL_PICS\Pictures for packshots - per team\Celebration\\"

import os

for count, filename in enumerate(os.listdir(DIR_PATH)[2:]):
    print(filename)
    src = DIR_PATH + filename
    if ("MPP" in filename):
        try:
            new_filename = filename.split("_")[1] + ".jpg"
            os.rename(src, DIR_PATH + new_filename)
        except FileExistsError as e:
            print(e)


