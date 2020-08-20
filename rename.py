import os

for count, filename in enumerate(os.listdir(r"E:\Ikea_Projekt\Results_JPG\HFB13")):
    src = r'E:\Ikea_Projekt\Results_JPG\HFB13\\' + filename
    a = filename.split("_")
    if (len(a[0])==2):
        a[0] = "0"+a[0]

    filename='_'.join(a)

    # rename() function will
    # rename all the files
    os.rename(src, r'E:\Ikea_Projekt\input_photos\HFB13\IN\\'+filename)