import os
import pydicom
import sys


def Desens(path):
    ds = pydicom.dcmread(path)
    ds.PatientName = ''
    ds.PatientSex = ''
    ds.PatientBirthDate = ''
    ds.InstitutionName = ''
    ds.InstitutionAddress = ''
    ds.save_as(path)


def TravDir(rootdir):
    filelist = os.listdir(rootdir)
    for i in range(0, len(filelist)):
        path = os.path.join(rootdir, filelist[i])
        if os.path.isdir(path):
            TravDir(path)
        if os.path.isfile(path):
            Desens(path)
    print('Successful')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        TravDir(sys.argv[1])
    else:
        print('Fail!')
