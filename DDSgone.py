import os
import time

# get filepath
print("======================================================")
print("Automatic dds remover/updater")
print("V0.1.1")
print("Made by: Jaspervdv")
print("======================================================")

while(True):
    path = input("path:")
    try:
        open(path + "\decals.json")
    except OSError:
        print("No decal json found")
    else:
        break

print("Monitoring " + path)

# find file age
decalTime = 0
sponsorTime = 0

try:
    open(path + "\decals.png")
except OSError:
    print("No decals.png found")
else:
    print("decals.png found")
    decalTime = os.stat(path + "\decals.png").st_mtime

try:
    open(path + "\sponsors.png")
except OSError:
    print("No sponsors.png found")
else:
    print("sponsors.png found")
    sponsorTime = os.stat(path + "\sponsors.png").st_mtime

# monitor file
while True:
    if decalTime != 0:
        newDecalTime = os.stat(path + "\decals.png").st_mtime

        if decalTime != newDecalTime:
            decalTime = newDecalTime

            try:
                os.remove(path + "\decals_0.dds")
                os.remove(path + "\decals_1.dds")
                os.remove(path + "\ponsors_0.dds")
                os.remove(path + "\ponsors_1.dds")
            except:
                continue

    # prevent overupdating
    time.sleep(1)
