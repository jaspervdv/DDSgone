import json
import os
import time

# get filepath
print("======================================================")
print("Automatic dds remover/updater")
print("V0.2.1")
print("Made by: Jaspervdv")
print("======================================================")

foundFile = True

while(True):
    path = input("path:")
    try:
        open(path + "\decals.json")
    except OSError:
        print("No decal json found")
    else:
        words = path.split('\\')
        setupPath = ""

        filterStrings = words[: words.index("Assetto Corsa Competizione") + 1]

        for filterString in filterStrings:
            setupPath += filterString + "\\"

        setupPath += "Config\\menuSettings.json"

        try:
            open(setupPath)
        except OSError:
            print("No menuSettings found")
            continue

        break

print()
print("Setup File " + setupPath)
print("Monitoring " + path)
print()

# uncheck texDDS in setting json
with open(setupPath, 'r+') as f:
    data = json.load(f)
    data['texDDS'] = 0
    f.seek(0)  # <--- should reset file position to the beginning.
    json.dump(data, f, indent=4)

try:
    os.remove(path + "\decals_0.dds")
    os.remove(path + "\decals_1.dds")
    os.remove(path + "\ponsors_0.dds")
    os.remove(path + "\ponsors_1.dds")

except OSError:
    pass

print("")
print("ACC can be started")
input("Press any key when finished:")

# check texDDS in setting json
with open(setupPath, 'r+') as f:
    data = json.load(f)
    data['texDDS'] = 1
    f.seek(0)  # <--- should reset file position to the beginning.
    json.dump(data, f, indent=4)

print("Process ended")
print("Window can be closed")
print("Please restart ACC")
time.sleep(20)
