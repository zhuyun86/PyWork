from PIL import Image
import os
import math
import itertools

path = r'./image/jd.png'
img = Image.open(path).convert('L')  #打开图片,convert图像类型有L,RGBA
img = img.resize((120,120))

def GetWinLevel(arr):
    return min(arr), max(arr), max(arr)-min(arr), sum(arr)/len(arr)

def GetBlockStyle(arr):
    tup = GetWinLevel(arr)
    if tup[2]<10:
        if tup[3]>50:
            return ' '
        else:
            return '*'
    else:
        if arr[0]>tup[3] and arr[1]>tup[3] and arr[2]<tup[3] and arr[3]<tup[3]:
            return '-'
        if arr[0]<tup[3] and arr[1]<tup[3] and arr[2]>tup[3] and arr[3]>tup[3]:
            return '-'
        if arr[0]>tup[3] and arr[1]<tup[3] and arr[2]>tup[3] and arr[3]<tup[3]:
            return '|'
        if arr[0]<tup[3] and arr[1]>tup[3] and arr[2]<tup[3] and arr[3]>tup[3]:
            return '|'
        if arr[0]>tup[3] and arr[1]<tup[3] and arr[2]<tup[3] and arr[3]<tup[3]:
            return '/'
        if arr[0]<tup[3] and arr[1]<tup[3] and arr[2]<tup[3] and arr[3]>tup[3]:
            return '/'
        if arr[0]<tup[3] and arr[1]>tup[3] and arr[2]>tup[3] and arr[3]>tup[3]:
            return '/'
            # return '┘'
        if arr[0]>tup[3] and arr[1]>tup[3] and arr[2]>tup[3] and arr[3]<tup[3]:
            return '/'
            # return '┌'
        if arr[0]<tup[3] and arr[1]>tup[3] and arr[2]<tup[3] and arr[3]<tup[3]:
            return '\\'
        if arr[0]<tup[3] and arr[1]<tup[3] and arr[2]>tup[3] and arr[3]<tup[3]:
            return '\\'
        if arr[0]>tup[3] and arr[1]<tup[3] and arr[2]>tup[3] and arr[3]>tup[3]:
            return '\\'
            # return '└'
        if arr[0]>tup[3] and arr[1]>tup[3] and arr[2]<tup[3] and arr[3]>tup[3]:
            return '\\'
            # return '┐'
        else:
            return ' '

if __name__ == '__main__':
    with open('./image/pixelation_{}.txt'.format(os.path.basename(os.path.splitext(path)[0])), 'w') as f: 
        for y in range(img.size[1]//2):
            for x in range(img.size[0]//2):
                quat = [img.getpixel((2*x, 2*y)), img.getpixel((2*x+1, 2*y)), img.getpixel((2*x, 2*y+1)), img.getpixel((2*x+1, 2*y+1))]
                f.write(GetBlockStyle(quat))
            f.write('\n')