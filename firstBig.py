#! /bin/python
import string, os, os.path, math, shutil

# list of directories which need to be synchronized with my machine
folder_list = ['/home/ramki/Desktop',
               '/home/ramki/Downloads',
               '/home/ramki/Documents',
               '/home/ramki/Pictures']

# Synchronising with my Dropbox directory on my machine
dropbox_folder = '/home/ramki/Dropbox'

os.chdir("/home/ramki/Dropbox/")


def filecreate(folder):
    if folder not in os.listdir(os.getcwd()) :
        os.mkdir(folder)
    else:
        pass

def delete_dir(root, temp, dirs):
    for i in dirs:
        if not os.path.exists(os.path.join(temp,i)) :
            shutil.rmtree(os.path.join(root,i),ignore_errors=True)

for root, dirs, files in os.walk(dropbox_folder):
    temp = root.replace('/home/ramki/Dropbox','/home/ramki/')
    delete_dir(root, temp, dirs)
    for name in files :
        if not os.path.exists(os.path.join(temp,name)) :
            os.remove(os.path.join(root,name))

def get_Dropbox_folder_size(dirpath):
    Total = 0
    for root, dirs, files in os.walk(dirpath):
        try:
            Total = Total + sum(os.path.getsize(os.path.join(root, name)) for name in files)
        except:
            pass
    return int(Total)

def temp_function(source_folder):
    file_mem = 0
    for root, dirs, files in os.walk(source_folder):
        temp = root.replace('/home/ramki/','/home/ramki/Dropbox/')
        for name in files :
            if os.path.exists(os.path.join(temp,name)) :
                if ( os.path.getmtime(os.path.join(root,name)) - os.path.getmtime(os.path.join(temp,name)) ) > 1 :
                    file_mem = file_mem + (os.path.getsize(os.path.join(root,name)) - (os.path.getsize(os.path.join(temp,name))))
            else:
                file_mem = file_mem + os.path.getsize(os.path.join(root,name))
    return file_mem

file_mem1 = 0
file_mem_total = 0
for folder in folder_list:
    file_mem1 = temp_function(folder)
    file_mem_total = file_mem_total + file_mem1
    print float(file_mem1/pow(2,20)), "MB needs to be syncronize from", folder

def create_dir(root, temp, dirs):
    for i in dirs:
        try:
            if not os.path.exists(os.path.join(temp,i)) :
                shutil.copytree(os.path.join(root,i), os.path.join(temp,i))
        except:
            pass

def sync_folder(source_folder):
    for root, dirs, files in os.walk(source_folder):
        temp = root.replace('/home/ramki/','/home/ramki/Dropbox/')
        create_dir(root, temp, dirs)
        try:
            for name in files :
                if os.path.exists(os.path.join(temp,name)) :
                    if ( os.path.getmtime(os.path.join(root,name)) - os.path.getmtime(os.path.join(temp,name)) ) > 1 :
                        shutil.copy2(os.path.join(root,name),temp)
                else:
                    shutil.copy2(os.path.join(root,name),temp)
        except:
            pass
if ((file_mem_total) < (pow(2,31) - (get_Dropbox_folder_size(dropbox_folder)))):
    [filecreate(os.path.basename(folder)) for folder in folder_list]
    for folder in folder_list:
        print "Syncronizing ", folder
        sync_folder(folder)
else:
    if ((file_mem_total) > (pow(2,31) - (get_Dropbox_folder_size(dropbox_folder)))):
        print (int((file_mem_total) - (pow(2,31) - (get_Dropbox_folder_size(dropbox_folder))))/(pow(2,20))),"MB Xrta space needed "

