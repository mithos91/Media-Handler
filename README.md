# Media-Handler
Hi there. I made this simple code that helps into extract and catalog your media files following these simple steps:
1. connect your HDD or SD or MicroSD or whatever you're using to stock your media files.
2. use the program and follow the instructiong
3. after the program finishes, you will have a folder in which all files are organized in subfolders: first folder gear type, then second subfolder video / photo / raw then
   if they are panoramas, they will have a folder within the photos or raws folder as well.
   
# In order to do that PAY ATTENTION TO THE FOLLOWING STEPS   

## Before:
### You should have python installed, but if you're here I'm expecting you already have. So move on.
### You should have these modules installed: win32api

## After:
1. open the file and look for **UPDATE THESE VALUES IF NEEDED**. This section is found at the top of the file.
2. Look for **dumppath** variable and edit it with your own path (the one you want your files to be copied)
3. **SUPER IMPORTANT**: Look for **ignorepaths** and remove/add/edit all those drivers you want not to be touched. Example C as maindrive, D as backup drive etc. 
   Those you don't need to do any sort of operation
4. Look for **directorynames**: my program works by searching all drivers that are currently connected on your PC, then if the drive's name is found in this list, it will copy the
   files. So, in order to do that, rename your drives, or update this list in order to be able to find these drive. All uppercase please.

## Bonus:
if you want to personalize this program to suit you better then:
5. **direxclutepanoramas** : this is a list where I grouped all the common names usually used as Panoramas. DJI usually names these folder PANORAMA, so feel free to add/edit/remove
   in order to suit you better
6. **allextension** : this is a list of all extension I'm interessed for. So if your device is able to produce different formats, just add/edit/remove this list
7. **foldergroup**  : this is a dictionary. For those not very used to pythons code, is more complex version of list. The one thing you should be interessed for is that every 
   subfolder is generated because there is an instruction in this dictionary. 
   Broken down to simplify this to you, it will create a folder VIDEO and it will copy all the MP4 files in it. As well for photos and etc. So don't edit if you're not very
   sure of what you're doing. But, feel free to edit it and re-arrange as you wish.
   
My site [numerable.it](www.numerable.it)
