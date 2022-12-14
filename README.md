# DDSgone

DDSgone is a simple program that is made to support the livery creation process in Assetto Corsa Competizione. DDSgone will remove the dds files of a selected livery and force ACC to ignore DDS files temporarily. This allows for direct livery updating in the garage, so no dds files have to be repeatedly removed and no config files have to manually edited. The program also has a simple memory function, allowing for quick access to known files/directories without the need to find the file paths for every use. 

DDSgone is has the DDSrestore and Lfilter tools integrated. DDSrestore will restore settings if DDSgone has encountered issues and LFilter will remove redundant livery directories in the ACC liveries directory.

.exe is occasionally seen as a trojan, sorry about that, it is not. However, if you want to be save you can run the .py files if you have python installed on your system.

# How to acquire the .exe files

If you have any familiarity with GitHub just move on to the next section. This section is for people with no programming background, for which this tool is mostly created.

1. Go to the directory structure located above and open the "dist" directory.

2. Open the desired .exe

3. Press the "download" button.

4. If your computer freaks out, do not worry, this is normal behavior when you download a random .exe file. In chrome: Press the arrow icon and click "keep".

5. When you start the .exe, again the computer can warn you, again this is normal behavior. Click "more info" followed by "run anyway"

# How to use DDSgone

DDSgone.exe (and .py) will remove the present dds files from a livery folder that is worked upon and temporarily suppress ACC from creating and using dds files. 

1. Run either the .exe or .py DDSgone file (before starting ACC). You are greeted with the main DDSgone window. From here you can access the main DDSgone processes but also the DDSrestore and Lfilter functionality (see their respective sections).
2. To enable the DDsgone functionality the tool requires the directory of the livery that is going to be edited. This can be submitted via a direct filepath, or via the browse button (example path: C:\Users\jaspe\Documents\Assetto Corsa Competizione\Customs\Liveries\Porsche_991_GT3_SCB_Emilia_415). 

![Start window](./Images/1_startwindow.JPG?raw=true "Start Window")

2. Press the "Open" button, if the file path is deemed correct the program will continue.

![Monitoring](./Images/2_correctpath.JPG?raw=true "Monitoring")

3. Open ACC and start editing the livery you selected.

!! **Do not close DDSgone, keep it running in the background** !! 

DDSgone does prevent accidental closing during this step. However, if the program is accidentally closed run DDSrestore.

![During Editing](./Images/3_liveryediting.JPG?raw=true "During Editing")

4. When finished editing the livery, close ACC and press the "End" button in DDSgone. Afterwards DDSgone can be terminated or another livery directory can be selected. After the process has been terminated ACC can restarted and played normally.

![Closing step](./Images/4_succes.JPG?raw=true "Closing Step")

5. The livery directories that have been submitted to DDSgone will be memorized. They are accessible via the arrow icon in the path prompt. DDSgone is able to memorize up to 10 paths.

![Safe to Close](./Images/5_memory.JPG?raw=true "Safe to Close")

## How to use DDSrestore

DDSrestore.exe (and .py) restores ACC settings that could be left set incorrectly by prematurely closing DDSgone.exe (and .py). This can only happen if the process is hard terminated (via process manager) or if the system on which it ran crashed. These incorrect settings could cause the big joining freezes of 2020/21 in multiplayer.

1. When in the main DDSgone window, press the "Restore" button.
2. This will open a new window where a filepath can be submitted. If you have used DDSgone before the path will be automatically filled in. If not set the path to the root folder of ACC (example path: C:\Users\jaspe\Documents\Assetto Corsa Competizione)

![Restore Start Window](./Images/6_restorepath.JPG?raw=true "Restore Start Window")

2. Press the "Restore" button. If successful DDSrestores will notify you and the window can be closed

![Restore Safe to Close](./Images/7_restoresucces.JPG?raw=true "Restore Safe to Close")

3. ACC can be restarted and used for playing.

# How to use LFilter

LFilter.exe (and .py) removes all the unused liveries directory from the ACC directory. Creating a better overview of all the liveries that are actually present. 

!!**currently recognized overlay files: .png, .jpg, .dds**!!

!!**Make a backup of the liveries folder before use, this program will permanently remove folders and files.**!!

1. When in the main DDSgone window, press the "Filter" button.
2. This will open a new window where a filepath can be submitted. If you have used DDSgone before the path will be automatically filled in. If not set the path to the root folder of ACC (example path: C:\Users\jaspe\Documents\Assetto Corsa Competizione).

![Filter Start Window](./Images/8_Lfilterpath.JPG?raw=true "Filter Start Window")

3. Press the "Filter" button. If successfull LFilter will notify you how many directories have been removed and the window can be closed.

![Filter Safe to Close](./Images/10_Lfiltersuccess.JPG?raw=true "Filter Safe to Close")
