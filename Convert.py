import os
import shutil
import sys

HospitalName = "Test"
SrcDir = r"C:\Users\12sigma\Desktop\bad"
TempDir = 'D:/Temp'
DstDir = 'D:/Nii_Output_' + HospitalName
ExeFile = r'C:\Users\12sigma\Desktop\test\exes\dcm2niix.exe'


def Convert(rootdir):
    dirList = os.listdir(rootdir)
    for i in range(0, len(dirList)):
        oldir = os.path.join(rootdir, dirList[i])

        if os.path.isdir(oldir):
            redir = oldir
            if ' ' in oldir:
                redir = oldir.replace(' ', '_')
                os.rename(oldir, redir)

            if os.path.exists(TempDir):
                shutil.rmtree(TempDir, True)
            os.mkdir(TempDir)

            os.system('{} {} {} {}_%f'.format(ExeFile, '-o', TempDir, redir))
            MoveMaxFile(TempDir)

            if os.path.exists(TempDir):
                shutil.rmtree(TempDir, True)

    print('Successful')


def MoveMaxFile(dir):
    fileList = os.listdir(dir)
    maxFile = ''
    maxSize = 0
    for i in range(0, len(fileList)):
        path = os.path.join(dir, fileList[i])
        size = os.path.getsize(path)
        maxFile = fileList[i] if size > maxSize else maxFile
        maxSize = size if size > maxSize else maxSize
    shutil.move(os.path.join(dir, maxFile), os.path.join(DstDir, maxFile))


if __name__ == '__main__':
    if not os.path.exists(DstDir):
        os.mkdir(DstDir)
    Convert(SrcDir)
