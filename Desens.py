import os
import pydicom
import sys, threading

def Desens(path):
    try:
        ds = pydicom.dcmread(path)
    except Exception as e:
        print('Error:', path, e)
        return
    ds.PatientName = ''
    ds.PatientSex = ''
    ds.PatientBirthDate = ''
    ds.InstitutionName = ''
    ds.InstitutionAddress = ''
    ds.save_as(path)
    print(path,'completed')


def TravDir(rootdir):
    filelist = os.listdir(rootdir)
    for i in range(0, len(filelist)):
        path = os.path.join(rootdir, filelist[i])
        if os.path.isdir(path):
            TravDir(path)
        if os.path.isfile(path):
            Desens(path)
    print('Successful')

def DoDesens(rootdir, cv):
    with cv:
        TravDir(rootdir)
        cv.notify()
        print('Desens:', threading.current_thread())



if __name__ == '__main__':
    if len(sys.argv) > 1:
        TravDir(sys.argv[1])
    else:
        print('Fail!')
