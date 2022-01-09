import os,sys,string,shutil,win32api,datetime

#UPDATE THESE VALUES IF NEEDED
##### Directory paste + handling
dumppath = 'C:\\Users\\anton\\Desktop\\TempMedia'
dumppathcompl = dumppath + '\\' + datetime.datetime.now().strftime("%d-%m-%Y")
ignorepaths = ['C','D']
directorynames = ['GOPRO','MINI 2','POCKET 2','NIKON','HERO8']
direxclutepanoramas = ['PANORAMA']
yesorno = ['Y','N']


#DO NOT MODIFY ANYTHING AFTER THIS POINT OR COULD LEAD TO POTENTIAL LOSSES
##### all directory variables
allpaths = list(string.ascii_uppercase) 

checkpaths = []
foundpaths = {}
directoryindex = ':\\'
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
filecounter = 0



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
        #create submain directory by date
        if not os.path.exists(dumppathcompl):
                os.makedirs(dumppathcompl)                
        #check which driver is plugged then create related folder
        for i in allpaths:
                path = i + ":\\\\"
                try:
                        devicename = win32api.GetVolumeInformation(str(path))[0]
                        devicename = devicename.upper()
                        for j in directorynames:
                                if j in devicename:
                                        newpathfolder = dumppathcompl + '\\' + j
                                        foundpaths[path] = {
                                                'PathPC'        :       newpathfolder,
                                                'Device'        :       j
                                                }
                                        if not os.path.exists(newpathfolder):
                                                os.makedirs(newpathfolder)
                except:
                        pass
    
############### SCAN FOR FILES AND REGISTER INTO A LIST
def scanformedia(filecounter):
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
                                
                                #SUPER IMPORTANT check if ext in list allowed are in filepath for creating folders
                                for mediatype in tempextension.keys():
                                        if tempextension[mediatype]['controller'] is False:
                                                if any(ext in filepath for ext in tempextension[mediatype]['Ext']):
                                                        tempextension[mediatype]['controller'] = True
                                                        
                                #SUPER IMPORTANT check if value to be excluded in list is present in the filepath
                                if any(valexc in filepath for valexc in direxclutepanoramas):
                                        for exti in allextension:
                                                if exti in filepath:
                                                        listoffilesondevices[filecounter] = {
                                                                'Name'          :       file,                   # filename
                                                                'Path'          :       filepath,               # root + filename origin
                                                                'Size'          :       filedim,                # file dimension
                                                                'Panorama'      :       True,                   # Is Panorama?
                                                                'Type'          :       exti,                   # Extension MP4, JPG...
                                                                'Device'        :       foundpaths[j]['Device'] # #Folder to be transfered
                                                                }
                                else:
                                        for exti in allextension:
                                                if exti in filepath:
                                                        listoffilesondevices[filecounter] = {
                                                                'Name'          :       file,                   
                                                                'Path'          :       filepath,
                                                                'Size'          :       filedim,
                                                                'Panorama'      :       False,
                                                                'Type'          :       exti,
                                                                'Device'        :       foundpaths[j]['Device']
                                                                }                                        

                                filecounter +=1
                createfolderbyfile(foundpaths[j]['PathPC'],tempextension)
        print(filecounter)

        

def createfolderbyfile(foundpath,tempextension):
        for i in tempextension.keys():
                if tempextension[i]['controller'] is True:
                        foldername = os.path.join(foundpath,i)
                        if not os.path.exists(foldername):
                                os.makedirs(foldername)
        

                                
def copymedias():
        totalfiles = len(listoffilesondevices.keys())
        if totalfiles > 0:
                ratio = 100 / totalfiles
                counter = 0
                for file in listoffilesondevices:
                        counter += 1
                        countbars = counter * ratio
                        os.system('cls')
                        print('...')
                        print('Copying files...' + '\t' + str(counter) +' / '+ str(totalfiles))
                        print(str(file) + '\t' + "File Size: " + str(round(float(listoffilesondevices[file]['Size']) / 1048576,2)) + ' Mb')
                        print('...')
                        print('|' * round(countbars) + '.' *round(((totalfiles-counter)*ratio)) + '\t' + str(round(countbars,1)) + '%' )
                                

                        for foldtype in foldergroup:
                                for ext in foldergroup[foldtype]['Ext']:
                                        #remove damaged files or trash
                                        if listoffilesondevices[file]['Size'] >= 10000:
                                                origin = listoffilesondevices[file]['Path']
                                                destination = os.path.join(dumppathcompl,listoffilesondevices[file]['Device'],foldtype)
                                                #check by type and if panorama false then copy in proper folder
                                                if listoffilesondevices[file]['Type'] == ext and listoffilesondevices[file]['Panorama'] is False:                                                                                                
                                                        shutil.copy2(origin,destination)
                                                        
                                                #if not check by type and if panorama true create subfolder for panoramas photos
                                                elif listoffilesondevices[file]['Type'] == ext and listoffilesondevices[file]['Panorama'] is True:
                                                        panosplit = str(listoffilesondevices[file]['Path']).split('\\')                                                
                                                        panodestination = os.path.join(destination,'PANORAMA',panosplit[len(panosplit)-2])
                                                        if not os.path.exists(panodestination):
                                                                os.makedirs(panodestination)
                                                        shutil.copy2(origin,panodestination)
        else:
                answertorestart = ''
                while answertorestart not in yesorno:
                        answertorestart = input("no files, process stopped. Try again? y/n \n")
                        answertorestart = answertorestart.upper()
                        if answertorestart == 'Y':
                                askcopyloop()
                        elif answertorestart =='N':
                                sys.exit()
                        else:
                                print('wrong command given. Please answer Y or N')

                
                                                
                                        
def formatsds():
        for path in foundpaths:
                print('formattazione ' + path + ' in corso...')
                shutil.rmtree(path, ignore_errors=True)
        



#Loops for input asking                                        
def askcopyloop():
        askcopy = input('Check for files and then proceed to copy on Desktop? y/n \n')
        askcopy = askcopy.upper()
        if askcopy == 'Y':
                scanforfileinpc()
                createdirectories()
                scanformedia(filecounter)
                copymedias()
        elif askcopy == 'N':
                sys.exit()
        else:
                print('wrong command given. Please answer Y or N')
                askcopyloop()

def askforformatloop():
        askforformat = input("do you want to format all plugged sd cards? y/n \n ")
        askforformat = askforformat.upper()
        if askforformat == 'Y':
                formatsds()
                print('...')
                print('All units were formatted.')
                print('...')
                input('End - Press key to close')
        elif askforformat == 'N':
                print('...')
                print('No unit was formatted. Files on sd cards yet')
                print('...')
                input('End - Press key to close')
        else:
                print('wrong command given. Please answer Y or N')
                askforformatloop()        

        



##### EXECUTE ORDERs

looping = False
while looping == False:
        askcopyloop()
        askforformatloop()
        answeringlooping = ''
        while answeringlooping not in yesorno:
                answeringlooping = input('Restart programm? y/n \n')
                answeringlooping = answeringlooping.upper()
                if answeringlooping == 'Y':
                        looping = False
                elif answeringlooping == 'N':
                        looping = True
                else:
                        print('Please insert the correct valuer Y or N')
                




#notes
        #loopa tutti i valori nella lista listoffiles, loopa tutti i valori in exclude, e se y e' in x, copia x#
        #avoidfile = [x for x in listoffiles for y in direxclutepanoramas if y in x]
        #filetocopy = [x for x in listoffiles for y in avoidfile if y not in x]

        #for i in foundpaths.keys():
         #       print(i)
          #      for j in filetocopy:                        
           #             if i in j:
            #                    pass
