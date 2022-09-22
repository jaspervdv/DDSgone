import json
import os
import shutil
import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo
import webbrowser


def not_implemented():
    showinfo(
        title='Info',
        message='Function is not yet implemented'
    )


def fade_root():
    browse_button['state'] = tk.DISABLED
    path_cb['state'] = tk.DISABLED
    open_button['state'] = tk.DISABLED
    text_window['state'] = tk.DISABLED
    menubar.entryconfig(0, state=tk.DISABLED)


def enable_root():
    browse_button['state'] = tk.NORMAL
    path_cb['state'] = tk.NORMAL
    open_button['state'] = tk.NORMAL
    text_window['state'] = tk.NORMAL


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
    if len(folder_path):
        path_cb.set(folder_path)


def f_browse_button():
    global filter_folder_path
    filter_folder_path = filedialog.askdirectory()

    if filter_folder_path:
        filter_entry_box.delete(0, END)
        filter_entry_box.insert(0, filter_folder_path)

    filter_window.focus_force()


def p_browse_button():
    global package_folder_path
    package_folder_path = filedialog.askdirectory(initialdir=path_cb.get())

    if package_folder_path:
        package_entry_box.set(package_folder_path)

    package_window.focus_force()


def r_browse_button():
    global repair_folder_path
    repair_folder_path = filedialog.askdirectory(initialdir=path_cb.get()) # TODO

    if repair_folder_path:
        repair_entry_box.delete(0, END)
        repair_entry_box.insert(0, repair_folder_path)

    repair_window.focus_force()


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

    else:
        showinfo(
            title='Info',
            message="No valid root directory found"
        )
        filter_window.lift()


def r_repair_button():
    r_setup_path = repair_entry_box.get() + "/Config/menuSettings.json"

    try:
        open(r_setup_path)
    except OSError:
        showinfo(
            title='Info',
            message="No settings file found"
        )
        repair_window.focus_force()
        return

    repair_text_window.insert(tk.END, "\n\nRestoring settings file: " + r_setup_path)

    with open(r_setup_path, 'r+') as f:
        data = json.load(f)
        data['texDDS'] = 1
        f.seek(0)  # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)

    repair_text_window.insert(tk.END, "\n\nSuccessfully restored settings ")


def help_call():
    webbrowser.open('https://github.com/jaspervdv/DDSgone/blob/master/README.md')


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


def package(to_zip, to_structure):
    if len(package_entry_box.get()):

        package_text_window.insert(tk.END, "\n\nCopying and packaging files")

        livery_path = package_entry_box.get()
        link_name = os.path.basename(livery_path)
        cars_path = os.path.dirname(os.path.dirname(livery_path)) + "/Cars"

        json_path = ""
        file = ""

        if os.path.isdir(cars_path):
            found = False
            for subdir, dirs, files in os.walk(cars_path):
                for file in files:
                    json_path = cars_path + '/' + file
                    with open(json_path, 'r', encoding='utf-16-le') as f:
                        customskinline = f.readlines()[29]
                        templatename = customskinline.split(":")[1][2:-3]

                        if link_name == templatename:
                            found = True
                            break
                            # make temp folder
                if found:
                    break

            if found:
                desk_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
                if to_structure.get():
                    temp_ex_folder = desk_path + "\\Assetto Corsa Competizione"
                    cars_structure_path = desk_path + "\\Assetto Corsa Competizione\\Customs\\Cars"
                    livery_structure_path = desk_path + "\\Assetto Corsa Competizione\\Customs\\Liveries\\" + link_name

                    os.makedirs(desk_path + "\\Assetto Corsa Competizione")
                    os.makedirs(desk_path + "\\Assetto Corsa Competizione\\Customs")
                    os.makedirs(cars_structure_path)
                    os.makedirs(desk_path + "\\Assetto Corsa Competizione\\Customs\\Liveries")
                    os.makedirs(livery_structure_path)

                    shutil.copyfile(json_path, cars_structure_path + "/" + file)

                    for subdir, dirs, files in os.walk(livery_path):
                        for file in files:
                            if os.path.splitext(file)[-1] != ".dds":
                                shutil.copyfile(livery_path + "/" + file, livery_structure_path +  "/" + file)

                    if to_zip.get():
                        shutil.make_archive(temp_ex_folder, 'zip', temp_ex_folder)
                        shutil.rmtree(temp_ex_folder)

                    return

                else:
                    temp_ex_folder = desk_path + "\\" + link_name
                    os.makedirs(temp_ex_folder)

                    # copy car json
                    shutil.copyfile(json_path, temp_ex_folder + "/" + file)

                    # copy livery files
                    os.makedirs(temp_ex_folder + "/" + link_name)
                    for subdir, dirs, files in os.walk(livery_path):
                        for file in files:
                            if os.path.splitext(file)[-1] != ".dds":
                                shutil.copyfile(livery_path + "/" + file, temp_ex_folder + "/" + link_name + "/" + file)

                    if to_zip.get():
                        shutil.make_archive(temp_ex_folder, 'zip', temp_ex_folder)
                        shutil.rmtree(temp_ex_folder)

                    package_text_window.insert(tk.END, "\n\nSuccessfully packaged files")
                    package_text_window.insert(tk.END, "\nZip is stored at: " + temp_ex_folder)

                return
        else:
            showinfo(
                title='Info',
                message="No Cars directory"
            )

            package_window.focus_force()

    else:
        showinfo(
            title='Info',
            message="No filepath input given"
        )

        package_window.focus_force()


def filter_button():
    # disable all buttons on the root
    fade_root()

    global filter_window
    filter_window = Toplevel(root)
    filter_window.title('Lfilter')
    filter_window.geometry('600x200')

    filter_window.protocol("WM_DELETE_WINDOW", filter_window.quit)

    global filter_entry_box
    filter_entry_box = ttk.Entry(filter_window)
    filter_path = get_rootdir()

    filter_entry_box.insert(0, filter_path)

    filter_browse_button = ttk.Button(
        filter_window,
        text='Browse',
        command=f_browse_button
    )

    filter_filter_button = ttk.Button(
        filter_window,
        text='Filter',
        command=f_filter_button
    )

    filter_close_button = ttk.Button(
        filter_window,
        text='Close',
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

    filter_text_window.insert(tk.END, "Lfilter will remove all the unused livery folders\n")
    filter_text_window.insert(tk.END, "\nBrowse to select ACC root folder")
    filter_window.focus_force()

    filter_window.mainloop()
    filter_window.destroy()

    # enable all buttons in the root
    enable_root()


def repair_button():
    # disable all buttons on the root
    fade_root()

    global repair_window
    repair_window = Toplevel(root)
    repair_window.title('DDSrestore')
    repair_window.geometry('600x200')

    repair_window.protocol("WM_DELETE_WINDOW", repair_window.quit)

    global repair_entry_box
    repair_entry_box = ttk.Entry(repair_window)
    filter_path = get_rootdir()

    repair_entry_box.insert(0, filter_path)

    repair_browse_button = ttk.Button(
        repair_window,
        text='Browse',
        command=r_browse_button
    )

    repair_filter_button = ttk.Button(
        repair_window,
        text='Restore',
        command=r_repair_button
    )

    repair_close_button = ttk.Button(
        repair_window,
        text='Close',
        command=repair_window.quit
    )

    # create text output
    global repair_text_window
    repair_text_window = tk.Text(repair_window, width=16, height=5)

    # place the widget
    repair_text_window.pack(side=TOP, anchor=NW, fill=BOTH, expand=True, padx=5, pady=(5, 0))

    repair_entry_box.pack(side=TOP, anchor=NW, fill=X, padx=5, pady=5)
    repair_close_button.pack(side=LEFT, padx=5, pady=(0, 5))
    repair_browse_button.pack(side=RIGHT, anchor=NE, padx=5, pady=(0, 5))
    repair_filter_button.pack(side=RIGHT, anchor=NE, pady=(0, 5))

    repair_text_window.insert(tk.END, "DDSrestore will restore the original ACC settings\n")
    repair_text_window.insert(tk.END, "\nBrowse to select ACC root folder")
    repair_window.focus_force()

    repair_window.mainloop()
    repair_window.destroy()

    # enable all buttons in the root
    enable_root()


def package_button():
    # disable all buttons on the root
    fade_root()

    global package_window

    wantszip = IntVar()
    wantszip.set(1)

    wantsstructure = IntVar()
    wantsstructure.set(0)

    package_window = Toplevel(root)
    package_window.title('Lpackage')
    package_window.geometry('600x200')

    package_window.protocol("WM_DELETE_WINDOW", package_window.quit)

    global package_entry_box
    package_entry_box = ttk.Combobox(package_window, textvariable=selected_path, width=144)

    package_entry_box['values'] = update_dict(memoryPath)

    package_browse_button = ttk.Button(
        package_window,
        text='Browse',
        command=p_browse_button
    )

    package_button = ttk.Button(
        package_window,
        text='Package',
        command= lambda : package(wantszip, wantsstructure)
    )

    package_close_button = ttk.Button(
        package_window,
        text='Close',
        command=package_window.quit
    )

    zip_check = ttk.Checkbutton(
        package_window,
        text='.zip',
        variable=wantszip
    )

    structure_check = ttk.Checkbutton(
        package_window,
        text='Structure',
        variable=wantsstructure
    )

    # create text output
    global package_text_window
    package_text_window = tk.Text(package_window, width=16, height=5)

    # place the widget
    package_text_window.pack(side=TOP, anchor=NW, fill=BOTH, expand=True, padx=5, pady=(5, 0))

    package_entry_box.pack(side=TOP, anchor=NW, fill=X, padx=5, pady=5)
    package_close_button.pack(side=LEFT, padx=5, pady=(0, 5))

    package_browse_button.pack(side=RIGHT, anchor=NE, padx=5, pady=(0, 5))
    package_button.pack(side=RIGHT, anchor=NE, pady=(0, 5))

    zip_check.pack(side=LEFT, padx=5, pady=(0, 5))
    structure_check.pack(side=LEFT, padx=5, pady=(0, 5))

    package_text_window.insert(tk.END, "Lpackage will collect and package a selected livery\n")
    package_text_window.insert(tk.END, "\nBrowse to select livery folder")
    package_window.focus_force()

    package_window.mainloop()
    package_window.destroy()

    # enable all buttons in the root
    enable_root()


version = "V0.4.0"

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

menubar = tk.Menu(root)
tool_menu = tk.Menu(menubar, tearoff=0)

tool_menu.add_command(
    label="Restore",
    command=repair_button
)

tool_menu.add_separator()

tool_menu.add_command(
    label="Filter",
    command=filter_button
)

tool_menu.add_command(
    label="Package",
    command=package_button
)

tool_menu.add_command(
    label="Unpackage",
    command=not_implemented
)

tool_menu.add_separator()

tool_menu.add_command(
    label="Livery management",
    command=not_implemented
)

help_menu = tk.Menu(menubar, tearoff=0)

help_menu.add_command(
    label="Help",
    command=help_call
)

help_menu.add_command(
    label="Settings",
    command=not_implemented
)

help_menu.add_separator()

help_menu.add_command(
    label="exit",
    command=root.destroy
)


menubar.add_cascade(label="Tools", menu=tool_menu)
menubar.add_cascade(label="Help", menu=help_menu)

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
text_window = tk.Text(root, width=16, height=5)

# place the widget
text_window.pack(side=TOP, anchor=NW, fill=BOTH, expand=True, padx=5, pady=(5, 5))
path_cb.pack(side=TOP, anchor=NW, fill=X, padx=5)
browse_button.pack(side=RIGHT, anchor=NE, padx=5, pady=5)
open_button.pack(side=RIGHT, anchor=NE, padx=0, pady=5)

root.config(menu=menubar)

# close splash when using .exe
try:
    import pyi_splash

    pyi_splash.update_text('UI Loaded ...')
    pyi_splash.close()
except:
    pass

text_window.insert(tk.END, "Select livery folder of the livery that is going to be edited\n")

root.mainloop()
