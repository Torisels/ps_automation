import shutil
import os


# the first walk would be the same main directory
# which if processed, is
# redundant
# and raises shutil.Error
# as the file already exists

# rem_dirs = walker.next()[1]


PATH = f'E:\IKEA_ALL_PICS\Pictures for packshots - per team\HFB 16'
# The current working directory
dest_dir = PATH
# The generator that walks over the folder tree
walker = os.walk(PATH)
for d in walker:
    for file in d[2]:
        try:
            shutil.copy(d[0] + os.sep + file, dest_dir)
        except Exception as e:
            print(e)

# for data in walker:
#     for files in data[2]:
#         try:
#             shutil.move(data[0] + os.sep + files, dest_dir)
#         except shutil.Error:
# # still to be on the safe side
# continue
#
# # clearing the directories
# # from whom we have just removed the files
# for dirs in rem_dirs:
#     shutil.rmtree(dest_dir + os.sep + dirs)
