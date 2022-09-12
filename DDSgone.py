import json
import os

import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo
from calendar import month_name

import easygui
import win32console, win32gui, win32con


def close_program():
    root.destroy()


def disable_event():
    pass


def browse_button():
    global folder_path
    folder_path = filedialog.askdirectory()
    path_cb.set(folder_path)

def end_button():
    # check texDDS in setting json
    with open(setupPath, 'r+') as f:
        data = json.load(f)
        data['texDDS'] = 1
        f.seek(0)  # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)

    # TODO update memory

    root.protocol("WM_DELETE_WINDOW", close_program)
    text_window.insert(tk.END, "\nProcess ended\n")
    text_window.insert(tk.END, "Window can be closed\n")
    text_window.insert(tk.END, "Please restart ACC\n")

    browse_button['state'] = tk.NORMAL
    path_cb['state'] = tk.NORMAL
    end_button.place_forget()
    open_button.place(x=817, y=370)

def open_button():
    if len(path_cb.get()) == 0:
        return

    #reset text window
    text_window.delete(1.0, tk.END)

    path = path_cb.get()

    # check if input is valid dir
    if not os.path.isdir(path):
        showinfo(
            title='Info',
            message='Not a valid path'
        )

    else:
        # check is potential livery file
        try:
            open(path + "\\decals.json")
        except OSError:
            showinfo(
                title='Info',
                message='No decal json found'
            )
        else:
            # check if new entry for mem
            if path_cb.current() == -1:
                words = path.split('/')
                global setupPath

                filterStrings = words[: words.index("Assetto Corsa Competizione") + 1]

                for filterString in filterStrings:
                    setupPath += filterString + "\\"

                setupPath += "Config\\menuSettings.json"

                try:
                    open(setupPath)
                except OSError:
                    showinfo(
                        title='Info',
                        message="No menuSettings found"
                    )
                    return
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

                        dictionary.insert(0, path)

                    dic = {
                        "tempFiles": dictionary
                    }

                    with open(memoryPath, 'w') as f:
                        json.dump(dic, f, indent=4)
            else:
                dictionary = []

                with open(memoryPath, 'r+') as f:
                    data = json.load(f)
                    dictionary = data['tempFiles']

                path = dictionary[path_cb.current()]
                words = path.split('/')
                setupPath = ""

                filterStrings = words[: words.index("Assetto Corsa Competizione") + 1]

                for filterString in filterStrings:
                    setupPath += filterString + "/"

                setupPath += "Config/menuSettings.json"

                del dictionary[path_cb.current()]
                dictionary.insert(0, path)

                dic = {
                    "tempFiles": dictionary
                }

                with open(memoryPath, 'w') as f:
                    json.dump(dic, f, indent=4)

        #call edit function
        browse_button['state'] = tk.DISABLED
        path_cb['state'] = tk.DISABLED
        open_button.place_forget()
        end_button.place(x=817, y=370)
        root.protocol("WM_DELETE_WINDOW", disable_event)

        text_window.insert(tk.END, "Setup File " + setupPath + "\n")
        text_window.insert(tk.END, "Monitoring " + path + "\n")
        text_window.insert(tk.END, "\nYou can now start ACC\nPress end when finished with livery editing\n")

        # uncheck texDDS in setting json
        with open(setupPath, 'r+') as f:
            data = json.load(f)
            data['texDDS'] = 0
            f.seek(0)
            json.dump(data, f, indent=4)

        try:
            os.remove(path + "/decals_0.dds")
            os.remove(path + "/decals_1.dds")
            os.remove(path + "/sponsors_0.dds")
            os.remove(path + "/sponsors_1.dds")

        except OSError:
            pass


version = "V0.3.1"

# get filepath
folder_path = ""
setupPath = ""
dictionary = []

# make a memory file if not yet present
memoryPath = os.getcwd()
memoryPath += "\\mem.json"

try:
    with open(memoryPath, 'r+') as f:
        data = json.load(f)
        dictionary = data['tempFiles']
        pass
except OSError:
    with open(memoryPath, 'w') as f:
        dic = {
            "tempFiles": []
        }
        json.dump(dic, f, indent=4)

useNewPath = True
windowPath = "*"

#make root window
root = tk.Tk()

# config the root window
root.geometry('900x400')
root.resizable(False, False)
root.title('DDSgone ' + version)

# create and populate recent file combobox
selected_path = tk.StringVar()
path_cb = ttk.Combobox(root, textvariable=selected_path, width=144)
path_cb['values'] = dictionary

# create browse button
browse_button = ttk.Button(
    root,
    text='Browse',
    command=browse_button
)

# create open button
open_button = ttk.Button(
    root,
    text='Open',
    command=open_button
)

# create end button (hidden
end_button = ttk.Button(
    root,
    text='End',
    command=end_button
)

# create text output
text_window = tk.Text(width=110, height=20)

# place the widget
text_window.place(x=5, y=5)
path_cb.place(x=5, y=343)
browse_button.place(x=735, y=370)
open_button.place(x=817, y=370)

root.mainloop()
