import json
while True:

    setupPath = input('ACC root folder path:')
    setupPath += "\\Config\\menuSettings.json"

    try:
        open(setupPath)
    except OSError:
        print("No settings file found")
    else:
        break

with open(setupPath, 'r+') as f:
    data = json.load(f)
    data['texDDS'] = 1
    f.seek(0)  # <--- should reset file position to the beginning.
    json.dump(data, f, indent=4)

print()
print("menuSettings restored")
print("Process ended")
print("Window can be closed")
print("Press enter to close window")
input()
