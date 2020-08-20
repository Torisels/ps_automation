import os

for count, filename in enumerate(os.listdir(r"E:\Ikea_Projekt\input_photos\HFB13\IN")):
    src = r'E:\Ikea_Projekt\input_photos\HFB13\IN\\' + filename
    filename = filename.replace(" ", "-")

    # rename() function will
    # rename all the files
    os.rename(src, r'E:\Ikea_Projekt\input_photos\HFB13\IN\\'+filename)