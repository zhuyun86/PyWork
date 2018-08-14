import os
import sys
import gzip
import shutil
import zipfile
import argparse


class CompressTool():
    def __init__(self):
        pass


def CompressNiiFile(path, outp):
    outfile = path.replace(os.path.dirname(path), outp)
    ls = os.path.splitext(outfile)
    if ls[1] != '.nii':
        return
    outfile = ls[0] + '.gz'
    with open(path, 'rb') as f_in:
        with gzip.open(outfile, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print('{} has compressed.'.format(path))


def DecompressNiiFile(path, outp):
    outfile = path.replace(os.path.dirname(path), outp)
    ls = os.path.splitext(outfile)
    if ls[1] != '.gz':
        return
    outfile = ls[0] + '.nii'
    with gzip.open(path, 'rb') as f_in:
        with open(outfile, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print('{} has decompressed.'.format(path))


def CompressDir(path):
    file_news = path + '.gz'
    with zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED) as z:
        for dirpath, dirnames, filenames in os.walk(path):
            fpath = dirpath.replace(path, '')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                z.write(os.path.join(dirpath, filename), fpath + filename)
                print('{} has compressed'.format(filename))
    print('All done!')


def TravDir(dirpath, outp, isCompress=True):
    for dirpath, dirnames, filenames in os.walk(dirpath):
        for filename in filenames:
            if isCompress:
                CompressNiiFile(os.path.join(dirpath, filename), outp)
            else:
                DecompressNiiFile(os.path.join(dirpath, filename), outp)
    print('All done!')


def CompressNii(path, outp, cv):
    with cv:
        if os.path.isdir(path):
            TravDir(path, outp)
        if os.path.isfile(path):
            CompressNiiFile(path, outp)
        cv.notify()


def DecompressNii(path, outp, cv):
    with cv:
        if os.path.isdir(path):
            TravDir(path, outp, False)
        if os.path.isfile(path):
            DecompressNiiFile(path, outp)
        cv.notify()


if __name__ == '__main__':

    path = sys.argv[1]
    if os.path.isdir(path):
        TravDir(path)
    if os.path.isfile(path):
        DecompressNiiFile(path)