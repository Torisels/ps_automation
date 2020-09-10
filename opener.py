import os

DIR_PATH = r"E:\Ikea_Projekt\Results_JPG\Celebration"

for count, filename in enumerate(os.listdir(DIR_PATH)[1:-2]):
    number = int(filename.split("_")[0])
    if number >= 20 and number <= 20:
        filename = filename.split(".")[0] + ".psd"
        print(filename)

        os.system("start " + r"E:\Ikea_Projekt\\" + filename)
