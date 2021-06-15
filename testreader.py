import os,sys,string,shutil,win32api

##### Directory paste + handling
dumppath = 'C:\\Users\\anton\\Desktop\\TempMedia'
temppath = dumppath+'\\_temp'



##### all directory variables
allpaths = list(string.ascii_uppercase) 
ignorepaths = ['C','D']
checkpaths = []
foundpaths = {}
directoryindex = ':\\'
directorynames = ['GOPRO','MINI 2','POCKET 2']
direxclutepanoramas = ['PANORAMA']
listoffilesondevices = {}
listoffilesonpc = {}

##### data handling variables:
allextension = ['MP4','JPG','JPEG','DNG','GPR','NEF']
foldergroup = {
        'Video'                 :       {
                'controller'    :       False,
                'Ext'           :       ['MP4']
                },
        'Photos'                :       {
                'controller'    :       False,
                'Ext'           :       ['JPG','JPEG']
                },
        'Raw'                   :       {
                'controller'    :       False,
                'Ext'           :       ['DNG','GPR','NEF']
                }
        }



#remove ignorepaths from allpaths
for i in ignorepaths:
        for j in allpaths:
                if j == i:
                        allpaths.remove(j)


############### SCAN FOR FILES ON PC AND REGISTER INTO A LIST
def scanforfileinpc():
        for root,dirs,files in os.walk(dumppath,topdown=True):
                for file in files:
                        filepath = os.path.join(root,file)
                        filedim = os.stat(filepath).st_size
                        listoffilesonpc[file] = {
                                'Path' : filepath,
                                'Size' : filedim
                                }

############### SCAN DEVICES, CREATE DIRECTORIES AND SUBDIRECTORIES
def createdirectories():
        #create main directory for dump files
        if not os.path.exists(dumppath):
                os.makedirs(dumppath)
        #check which driver is plugged then create related folder
        for i in allpaths:
                path = i + ":\\\\"
                try:
                        devicename = win32api.GetVolumeInformation(str(path))[0]
                        devicename = devicename.upper()
                        for j in directorynames:
                                if j in devicename:
                                        newpathfolder = dumppath + '\\' + j
                                        foundpaths[path] = {
                                                'PathPC'        :       newpathfolder,
                                                'Device'        :       j
                                                }
                                        if not os.path.exists(newpathfolder):
                                                os.makedirs(newpathfolder)                                        
                except:
                        pass

    
############### SCAN FOR FILES AND REGISTER INTO A LIST
def scanformedia():
        #use the list above to go to directories (safe handling)
        for j in foundpaths.keys():
                #create dict for folder creation:
                tempextension = foldergroup
                
                #scan directory
                for root,dirs,files in os.walk(j,topdown=True):
                        
                        #for each file create path + scan if folder
                        for file in files:                                
                                filepath = os.path.join(root,file)
                                filedim = os.stat(filepath).st_size
                                
                                #SUPER IMPORTANT check if ext in list allowed are in filepath
                                for mediatype in tempextension.keys():
                                        if tempextension[mediatype]['controller'] is False:
                                                if any(ext in filepath for ext in tempextension[mediatype]['Ext']):
                                                        print('false')
                                                        tempextension[mediatype]['controller'] = True
                                                        
                                #SUPER IMPORTANT check if value to be excluded in list is present in the filepath
                                if any(valexc in filepath for valexc in direxclutepanoramas):
                                        for exti in allextension:
                                                if exti in filepath:
                                                        listoffilesondevices[file] = {
                                                                'Path'          :       filepath,               # root + filename origin
                                                                'Size'          :       filedim,                # file dimension
                                                                'Panorama'      :       True,                   # Is Panorama?
                                                                'Type'          :       exti,                   # Extension MP4, JPG...
                                                                'Device'        :       foundpaths[j]['Device'] # #Folder to be transfered
                                                                }
                                else:
                                        for exti in allextension:
                                                if exti in filepath:
                                                        listoffilesondevices[file] = {
                                                                'Path'          :       filepath,
                                                                'Size'          :       filedim,
                                                                'Panorama'      :       False,
                                                                'Type'          :       exti,
                                                                'Device'        :       foundpaths[j]['Device']
                                                                }                                        
                                        
                createfolderbyfile(foundpaths[j]['PathPC'],tempextension)

        

def createfolderbyfile(foundpath,tempextension):
        for i in tempextension.keys():
                if tempextension[i]['controller'] is True:
                        foldername = os.path.join(foundpath,i)
                        if not os.path.exists(foldername):
                                os.makedirs(foldername)
        

                                
def copymedias():
        totalfiles = len(listoffilesondevices.keys())
        ratio = 100 / totalfiles
        counter = 0
        for file in listoffilesondevices:
                counter += 1
                countbars = counter * ratio
                print('|' * round(countbars) + '.' *round(((totalfiles-counter)*ratio)))
                for foldtype in foldergroup:
                        for ext in foldergroup[foldtype]['Ext']:
                                if listoffilesondevices[file]['Type'] == ext:
                                        origin = listoffilesondevices[file]['Path']
                                        destination = os.path.join(dumppath,listoffilesondevices[file]['Device'],foldtype)
                                        #shutil.copy2(origin,destination)
                                        
        
        pass
        #loopa tutti i valori nella lista listoffiles, loopa tutti i valori in exclude, e se y e' in x, copia x#
        #avoidfile = [x for x in listoffiles for y in direxclutepanoramas if y in x]
        #filetocopy = [x for x in listoffiles for y in avoidfile if y not in x]

        #for i in foundpaths.keys():
         #       print(i)
          #      for j in filetocopy:                        
           #             if i in j:
            #                    pass
        
        



##### EXECUTE ORDERs
createdirectories()
scanforfileinpc()
scanformedia()
copymedias()

#shutil.copytree(src, dst, symlinks=False, ignore=None, copy_function=copy2, ignore_dangling_symlinks=False, dirs_exist_ok=False)¶

#lista di video, fotos e raws


def molascioquaperdopo():
        #exclude panorama photos
                                for exclude in direxclutepanoramas:
                                        if exclude in root:
                                                print(filepath)
                                                continue
                                        
                                shutil.copy2(filepath,foundpaths[i])
