import json
import os
import shutil
import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo


def get_rootdir():
    # get predicted file location
    with open(memoryPath, 'r+') as f:
        data = json.load(f)
        dictionary = data['tempFiles']

    if len(dictionary) != 0:
        return str(os.path.dirname(os.path.dirname(os.path.dirname(dictionary[0]))))
    else:
        return str("")


def update_dict(memory_path):
    try:
        with open(memory_path, 'r+') as f:
            data = json.load(f)
            return data['tempFiles']
    except OSError:
        with open(memory_path, 'w') as f:
            dic = {
                "tempFiles": []
            }
            json.dump(dic, f, indent=4)
            return []


def close_program():
    root.destroy()


def disable_event():
    pass


def browse_button():
    global folder_path
    folder_path = filedialog.askdirectory()
    path_cb.set(folder_path)


def f_browse_button():
    global filter_folder_path
    filter_folder_path = filedialog.askdirectory()
    filter_entry_box.delete(0, END)
    filter_entry_box.insert(0, filter_folder_path)
    filter_window.lift()


def f_filter_button():
    f_setup_path = filter_entry_box.get() + "/Customs/Liveries"

    if os.path.isdir(f_setup_path):
        del_count = 0

        filter_text_window.insert(tk.END, "\n\nremoving redundant files from: " + f_setup_path)

        for subdir, dirs, files in os.walk(f_setup_path):
            found = False

            if subdir == f_setup_path:
                continue

            for file in files:
                ext = str(file[-4:])

                if ext == ".png" or ext == ".jpg" or ext == ".dds":
                    found = True
                    break

            if not found:
                del_count += 1
                for file in files:
                    pass
                    os.remove(os.path.join(subdir, file))
                shutil.rmtree(subdir)

        if del_count:
            filter_text_window.insert(tk.END, "\n\nSuccesfully removed " + str(del_count) + " folders")
        else:
            filter_text_window.insert(tk.END, "\n\nNo redundant directories have been found")

        filter_window.lift()
        # TODO make end button


    else:
        showinfo(
            title='Info',
            message="No valid root directory found"
        )
        filter_window.lift()


def end_button():
    # check texDDS in setting json
    with open(setupPath, 'r+') as f:
        data = json.load(f)
        data['texDDS'] = 1
        f.seek(0)  # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)

    # update memory
    path_cb['values'] = update_dict(memoryPath)

    root.protocol("WM_DELETE_WINDOW", close_program)
    text_window.insert(tk.END, "\nProcess ended\n")
    text_window.insert(tk.END, "Window can be closed\n")
    text_window.insert(tk.END, "Please restart ACC\n")

    # restore buttons to normal state
    browse_button['state'] = tk.NORMAL
    path_cb['state'] = tk.NORMAL
    filter_button['state'] = tk.NORMAL
    restore_button['state'] = tk.NORMAL
    end_button.pack_forget()
    open_button.pack(side=RIGHT, anchor=NE, padx=0, pady=5)


def open_button():
    if len(path_cb.get()) == 0:
        showinfo(
            title='Info',
            message='No filepath input given'
        )
        return

    # reset text window
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
                setupPath = ""

                filter_strings = words[: words.index("Assetto Corsa Competizione") + 1]

                for filterString in filter_strings:
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
                with open(memoryPath, 'r+') as f:
                    data = json.load(f)
                    dictionary = data['tempFiles']

                path = dictionary[path_cb.current()]
                words = path.split('/')
                setupPath = ""

                filter_strings = words[: words.index("Assetto Corsa Competizione") + 1]

                for filterString in filter_strings:
                    setupPath += filterString + "/"

                setupPath += "Config/menuSettings.json"

                del dictionary[path_cb.current()]
                dictionary.insert(0, path)

                dic = {
                    "tempFiles": dictionary
                }

                with open(memoryPath, 'w') as f:
                    json.dump(dic, f, indent=4)

        # call edit function
        browse_button['state'] = tk.DISABLED
        path_cb['state'] = tk.DISABLED
        filter_button['state'] = tk.DISABLED
        restore_button['state'] = tk.DISABLED

        open_button.pack_forget()
        end_button.pack(side=RIGHT, anchor=NE, padx=0, pady=5)
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


def filter_button():
    # disable all buttons on the root
    browse_button['state'] = tk.DISABLED
    path_cb['state'] = tk.DISABLED
    filter_button['state'] = tk.DISABLED
    restore_button['state'] = tk.DISABLED
    open_button['state'] = tk.DISABLED
    text_window['state'] = tk.DISABLED

    global filter_window
    filter_window = Toplevel(root)
    filter_window.title('DDSfilter')
    filter_window.geometry('600x200')

    filter_window.protocol("WM_DELETE_WINDOW", filter_window.quit)

    global filter_entry_box
    filter_entry_box = ttk.Entry(filter_window)
    filter_path = get_rootdir()

    filter_entry_box.insert(0, filter_path)

    filter_browse_button = ttk.Button(
        filter_window,
        text='browse',
        command=f_browse_button
    )

    filter_filter_button = ttk.Button(
        filter_window,
        text='filter',
        command=f_filter_button
    )

    filter_close_button = ttk.Button(
        filter_window,
        text='close',
        command=filter_window.quit
    )

    # create text output
    global filter_text_window
    filter_text_window = tk.Text(filter_window, width=16, height=5)

    # place the widget
    filter_text_window.pack(side=TOP, anchor=NW, fill=BOTH, expand=True, padx=5, pady=(5, 0))

    filter_entry_box.pack(side=TOP, anchor=NW, fill=X, padx=5, pady=5)
    filter_close_button.pack(side=LEFT, padx=5, pady=(0, 5))
    filter_browse_button.pack(side=RIGHT, anchor=NE, padx=5, pady=(0, 5))
    filter_filter_button.pack(side=RIGHT, anchor=NE, pady=(0, 5))

    filter_text_window.insert(tk.END, "DDSfilter will remove all the unused livery folders\n")
    filter_text_window.insert(tk.END, "\nBrowse to select ACC root folder")

    filter_window.mainloop()
    filter_window.destroy()

    # enable all buttons in the root
    browse_button['state'] = tk.NORMAL
    path_cb['state'] = tk.NORMAL
    filter_button['state'] = tk.NORMAL
    restore_button['state'] = tk.NORMAL
    open_button['state'] = tk.NORMAL
    text_window['state'] = tk.NORMAL


def repair_button():
    pass


version = "V0.3.2"

# get filepath
folder_path = ""
setupPath = ""

# make a memory file if not yet present
memoryPath = os.getcwd() + "\\mem.json"
windowPath = "*"

# make root window
root = tk.Tk()

# config the root window
root.geometry('900x400')
root.resizable(True, True)
root.title('DDSgone ' + version)

try:
    open('./images/logoSmall.ico')
except OSError:
    try:
        open('../images/logoSmall.ico')
    except OSError:
        pass
    else:
        root.iconbitmap(r'../images/logoSmall.ico')
else:
    root.iconbitmap(r'./images/logoSmall.ico')

# create and populate recent file combobox
selected_path = tk.StringVar()
path_cb = ttk.Combobox(root, textvariable=selected_path, width=144)
path_cb['values'] = update_dict(memoryPath)

# create browse button
browse_button = ttk.Button(
    root,
    text='Browse',
    command=browse_button
)

filter_button = ttk.Button(
    root,
    text='Filter',
    command=filter_button
)

restore_button = ttk.Button(
    root,
    text='Repair',
    command=repair_button
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
text_window = tk.Text(root, width=16, height=5)

# place the widget
text_window.pack(side=TOP, anchor=NW, fill=BOTH, expand=True, padx=5, pady=(5, 5))
path_cb.pack(side=TOP, anchor=NW, fill=X, padx=5)
filter_button.pack(side=LEFT, padx=5, pady=5)
restore_button.pack(side=LEFT)
browse_button.pack(side=RIGHT, anchor=NE, padx=5, pady=5)
open_button.pack(side=RIGHT, anchor=NE, padx=0, pady=5)

# close splash when using .exe
try:
    import pyi_splash

    pyi_splash.update_text('UI Loaded ...')
    pyi_splash.close()
except:
    pass

text_window.insert(tk.END, "Select livery folder of the livery that is going to be edited\n")

root.mainloop()
