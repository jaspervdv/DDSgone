# DDSgone

DDSgone is a simple program that is made to support the livery creation process in Assetto Corsa Competizione. DDSgone will remove the dds files of a selected livery and force ACC to ignore DDS files temporarily. This allows for direct livery updating in the garage, so no dds files have to be repeatedly removed and no config files have to manually edited. The program also has a simple memory function, allowing for quick access without the need to type or paste in file paths for every use. 

DDSgone is supported by DDSrestore and LFilter. DDSrestore will restore settings if DDSgone has encountered issues and LFilter will remove redundant livery directories in the ACC liveries directory.

.exe is occasionally seen as a trojan, sorry about that, it is not

# How to use DDSgone

DDSgone.exe (and .py) will remove the present dds files from a livery folder that is worked upon and temporarily suppress ACC from creating and using dds files. 

1. Run either the .exe or .py DDSgone file and set the path to the folder that has the livery data (example path: C:\Users\jaspe\Documents\Assetto Corsa Competizione\Customs\Liveries\Porsche_991_GT3_SCB_Emilia_415). 

![Start window](./Images/1_startwindow.JPG?raw=true "Start Window")

2. Press enter, if the file path is deemed correct the program will continue.

![Monitoring](./Images/2_correctpath.JPG?raw=true "Monitoring")

3. Open ACC and start editing the livery you selected.

!! **Do not close DDSgone, keep it running in the background** !! 

DDSgone does prevent accidental closing during this step. However, if the program is accidentally closed run DDSrestore.

![During Editing](./Images/3_liveryediting.JPG?raw=true "During Editing")

4. When finished editing the livery, close ACC and press enter in DDSgone. Afterwards DDSgone can be terminated by pressing enter. After the process has been terminated ACC can be played.

![Closing step](./Images/4_succes.JPG?raw=true "Closing Step")

5. At the next start of DDSgone you will be prompted with the option to open a recent file. If desired answer with y (enter) followed by the number of the desired file. DDSgone will memorize and order 10 file paths max

![Safe to Close](./Images/5_memory.JPG?raw=true "Safe to Close")

## How to use DDSrestore

DDSrestore.exe (and .py) restores ACC settings that could be left set incorrectly by prematurely closing DDSgone.exe (and .py). This can only happen if the process is hard terminated (via process manager) or if the system on which it ran crashed. These incorrect settings could cause the big joining freezes of 2020/21 in multiplayer.

1. Run either the .exe or .py DDSrestore file and set the path to the root folder of ACC (example path: C:\Users\jaspe\Documents\Assetto Corsa Competizione)

![Restore Start Window](./Images/6_restorepath.JPG?raw=true "Restore Start Window")

2. If successful DDSrestores will notify you and the window can be closed

![Restore Safe to Close](./Images/7_restoresucces.JPG?raw=true "Restore Safe to Close")

3. ACC can be restarted and used for playing

# How to use LFilter

LFilter.exe (and .py) removes all the unused liveries directory from the ACC directory. Creating a better overview of all the liveries that are actually present. 

!!**currently recognized overlay files: .png, .jpg, .dds**!!

!!**Make a backup of the liveries folder before use, this program will permanently remove folders and files.**!!

1. Run either the .exe or .py LFilter and set the path to the ACC root file folder (example path: C:\Users\jaspe\Documents\Assetto Corsa Competizione).

![Filter Start Window](./Images/8_Lfilterpath.JPG?raw=true "Filter Start Window")

2. You will be asked if the liveries directory is the correct path. Press y (enter) if it is, Press n(enter) if not.

![Filter Security](./Images/9_Lfilterlocation.JPG?raw=true "Filter Security")

3. If succesful LFilter will notify you how many directories have been removed and that the window can be closed.

![Filter Safe to Close](./Images/10_Lfiltersuccess.JPG?raw=true "Filter Safe to Close")
