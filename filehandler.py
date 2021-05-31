import os,sys,string,shutil


#folder to dump files
dumppath = 'C:\\Users\\anton\\Desktop\\TempMedia'
temppath = dumppath+'\\_temp'

#directory guidance
allpaths = list(string.ascii_uppercase) 
ignorepaths = ['C','D',]
checkpaths = []
directoryindex = ':\\'

#look for media signed by gear
allextension = ['JPG','JPEG','MP4','DNG','GPR','NEF']
searchfor = ['GOPRO','DJI','NIKON','D5200']
fileext = {
        'NIKON' : ['DSC'],
        'GOPRO' : ['GH','GOPR'],
        'DJI' : ['DJI']
        }
foundgear = []

#tempdatabse for file transfer:
tempdata = []


#create list exluding ignorepaths:
def updatelist():
        for i in allpaths:
                if i in ignorepaths:
                        pass
                else:
                        checkpaths.append(i)


#crawl all dir not to be ignore and look for searchfor parameters
def checker():
        for i in checkpaths:
                try:
                        path = str(i) + directoryindex
                        for root,dirs,files in os.walk(path,topdown=True):
                                for z in files:
                                        for j in allextension:
                                                if j in z:
                                                        shutil.copy2(root+'\\'+z, temppath)
                        cleansds(path)
                        


              
                except OSError as e:
                        print(e.strerror)
                        pass

#clean SDs
def cleansds(path):
        shutil.rmtree(path, ignore_errors=True)

#create directory based on file name
def analyzefiles():
        extfound = []
        for i in os.listdir(temppath):
                for gear, name in fileext.items():
                        for j in name:
                                if str(j) in str(i):
                                        if str(gear) not in foundgear:
                                                foundgear.append(gear)
                                        tempdata.append([gear,i])                                         
        createfolder(foundgear)

#create folder if a match is found within searchfor list
def createfolder(foundgear):
        for i in foundgear:
                if not os.path.exists(dumppath+'\\'+i):
                        os.makedirs(dumppath+'\\'+i)

def sortdata():
        for i in tempdata:
                for j in os.listdir(dumppath):
                        if str(i[0]) in (j):
                                print(temppath+'\\'+i[1])
                                shutil.copy2(temppath+'\\'+i[1], dumppath + '\\' + j)
        cleansds(temppath)
        

        

updatelist()

if not os.path.exists(temppath):
        os.makedirs(temppath)

checker()
analyzefiles()
sortdata()







#1 scan folder
#2 check for any searchfor
#3 if no check found and folder found
#4 scan subfolder go to 2
