import os
import shutil

print("======================================================")
print("Automatic liveries folder cleaner")
print("V0.0.1")
print("Made by: Jaspervdv")
print("======================================================")
print()

while True:

    setupPath = input('ACC root folder path:')
    setupPath += "\\Customs\\Liveries"

    con = False

    if(os.path.isdir(setupPath)):
        print("Valid liveries directory is found: " + setupPath)

        while True:
            answer = input("continue? (y/n):")
            if answer == 'Y' or answer == 'y':
                con = True
                break

            if answer == 'N' or answer == 'n':
                break
    else:
        print("Valid liveries directory cannot be found")

    if con == True:
        break

delCount = 0

for subdir, dirs, files in os.walk(setupPath):
    found = False

    if subdir == setupPath:
        continue

    for file in files:
        ext = str(file[-4:])

        if ext == ".png" or ext == ".jpg" or ext == ".dds":
            found = True
            break

    if found != True:
        delCount += 1
        for file in files:
            pass
            os.remove(os.path.join(subdir, file))
        shutil.rmtree(subdir)

print()
print("Succesfully removed " + str(delCount) + " folders")
print("Press enter to close window")
input()
