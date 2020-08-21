DIR_PATH = r"E:\IKEA_ALL_PICS\Pictures for packshots - per team\\"

import os

for count, filename in enumerate(os.listdir(DIR_PATH)[2:]):
    src = DIR_PATH + filename
    a = filename.split("B")
    if (len(a[1]) == 1):
        a[1] = "0" + a[1]
        filename = 'B'.join(a)
        os.rename(src, DIR_PATH + filename)


