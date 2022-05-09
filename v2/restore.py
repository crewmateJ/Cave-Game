from os import listdir
import json
"""

    THIS FUNCTION MIGRATES THE EXISTING MAPS
    note: make sure the folder 'v2' is in the original 'Cave Game' folder


"""
def restore():
    # check if it needs to be restored
    with open('v2.json', 'r') as f:
        has_restored = json.load(f)["has_restored"]
        if has_restored == "True":
            return

    print("Migrating old csv files...")

    # old filenames
    old_csv = [f for f in listdir("../") if "map" in str(f) and "csv" in str(f)]
    for file in old_csv:
        # get the old data
        old_file_directory = "../" + file
        old_file = open(old_file_directory, "r")

        coords = old_file.readline()
        x = old_file.readline().strip('\n').split(',')
        y = old_file.readline().strip('\n').split(',')
        old_file.close()

        # write new csv file 
        new_file_directory = "v2_" + file
        new_file = open(new_file_directory, "w")

        # top line is coords
        new_file.write(coords)

        # this time, (x, y) will be 1 pair per row
        # (previously all x coords on one line, all y coords on the next)
        for i in range(min(len(x), len(y))):
            line = x[i] + ',' + y[i] + '\n'
            new_file.write(line)

        print("Moved over " + file)

    with open('v2.json', 'w') as f:
        f.write('{"has_restored":"True"}')
    return