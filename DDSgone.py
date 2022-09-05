import json
import os
import win32console, win32gui, win32con

print("======================================================")
print("Automatic dds remover/updater")
print("V0.2.2")
print("Made by: Jaspervdv")
print("======================================================")
print()

# get filepath
path = ""
setupPath = ""

# make a memory file if not yet present
memoryPath = os.getcwd()
memoryPath += "\\mem.json"

try:
    with open(memoryPath, 'r+') as f:
        pass
except OSError:
    with open(memoryPath, 'w') as f:
        dic = {
            "tempFiles": []
        }
        json.dump(dic, f, indent=4)

useNewPath = True

#display options
with open(memoryPath, 'r') as f:
    data = json.load(f)
    dictionary = data['tempFiles']

    if len(dictionary) == 0:
        pass
    else:
        print("Recent files:")
        count = 1
        for i in reversed(dictionary):
            print(str(count) + " : " + i)
            count += 1

        print()
        while True:
            answer = input("Use recent file? (y/n): ")
            if answer == 'Y' or answer == 'y':
                useNewPath = False
                break
            if answer == 'N' or answer == 'n':
                break

            print("input y/n")


# get filepath if new file is needed
if useNewPath:
    while True:
        path = input("path:")
        try:
            open(path + "\\decals.json")
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
            else:
                # new entry in memory
                with open(memoryPath, 'r') as f:
                    data = json.load(f)
                    dictionary = data['tempFiles']

                if path in dictionary:
                    idx = dictionary.index(path)

                    del dictionary[idx]
                    dictionary.append(path)

                else:
                    if len(dictionary) > 10:
                        del dictionary[0]

                    dictionary.append(path)

                dic = {
                    "tempFiles": dictionary
                }

                with open(memoryPath, 'w') as f:
                    json.dump(dic, f, indent=4)

            break
else:
    dictionary = []

    with open(memoryPath, 'r+') as f:
        data = json.load(f)
        dictionary = data['tempFiles']

    while True:
        idx = int(input("enter number: "))

        if 0 < idx <= len(dictionary):
            break

        print("please enter a valid number")

    path = dictionary[len(dictionary) - idx]
    words = path.split('\\')
    setupPath = ""

    filterStrings = words[: words.index("Assetto Corsa Competizione") + 1]

    for filterString in filterStrings:
        setupPath += filterString + "\\"

    setupPath += "Config\\menuSettings.json"

    del dictionary[len(dictionary) -idx]
    dictionary.append(path)


    dic = {
        "tempFiles": dictionary
    }

    with open(memoryPath, 'w') as f:
        json.dump(dic, f, indent=4)

print()
print("Setup File " + setupPath)
print("Monitoring " + path)
print()

hwnd = win32console.GetConsoleWindow()
if hwnd:
    hMenu = win32gui.GetSystemMenu(hwnd, 0)
    if hMenu:
        win32gui.DeleteMenu(hMenu, win32con.SC_CLOSE, win32con.MF_BYCOMMAND)

# uncheck texDDS in setting json
with open(setupPath, 'r+') as f:
    data = json.load(f)
    data['texDDS'] = 0
    f.seek(0)  # <--- should reset file position to the beginning.
    json.dump(data, f, indent=4)

try:
    os.remove(path + "\\decals_0.dds")
    os.remove(path + "\\decals_1.dds")
    os.remove(path + "\\ponsors_0.dds")
    os.remove(path + "\\ponsors_1.dds")

except OSError:
    pass

print("")
print("ACC can be started")
input("Press any key when finished with livery creation:")

# check texDDS in setting json
with open(setupPath, 'r+') as f:
    data = json.load(f)
    data['texDDS'] = 1
    f.seek(0)  # <--- should reset file position to the beginning.
    json.dump(data, f, indent=4)

print("Process ended")
print("Window can be closed")
print("Please restart ACC")

print()
print("press any key to close window")
input()
