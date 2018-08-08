import sys
import os
import time
import random
from multiprocessing import Process

#from ztest import tet
import base64
import struct
import hashlib
import itertools
import psutil
import requests
from bs4 import BeautifulSoup
import sqlite3
import functools


def test1(bar=[]):
    bar.append('bar')

    headers = {
        'User-Agent':
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    }
    params = {'expect': 100}

    ssion = requests.session()

    r = ssion.get('http://datachart.500.com/ssq/?expect=100', headers=headers)
    requests.get('www.baidu.com')

    print(r.encoding)
    r.encoding = 'gb2312'
    print(r.encoding)

    bs = BeautifulSoup(r.content, 'lxml')
    print(bs.title.name)
    print(bs.title)
    print(bs.title.text)
    print(bs.meta)
    print(bs.meta.attrs)
    print(bs.meta['content'])

    with open('./record.txt', 'w') as file:
        rank = bs.find('tbody', attrs={'id': 'tdata'})
        if not rank:
            return

        for tr in rank.find_all('tr'):
            no = tr.find('td', align='center')
            if not no:
                continue

            no = no.text
            rb = [0] * 6
            i = 0
            for ball in tr.find_all('td', class_='chartBall01'):
                rb[i] = ball.text
                i = i + 1

            bb = tr.find('td', class_='chartBall02').text

            file.write('{}:\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
                no, rb[0], rb[1], rb[2], rb[3], rb[4], rb[5], bb))

    # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    # for i in bs.find_all('a'):
    #     print(i.string)

    return bar

    beg = time.time()
    time.sleep(random.random() * 10)
    end = time.time()
    print("Time is {}".format(end - beg))


def _test():
    response = requests.get("https://www.baidu.com/")
    #  返回CookieJar对象:
    cookiejar = response.cookies
    #  将CookieJar转为字典：
    cookiedict = requests.utils.dict_from_cookiejar(cookiejar)
    print("cookiejar:", cookiejar)
    print("cookiedict", cookiedict)


def __test():
    print("{2}{0}{1}".format(1, "fdd", 1.2323))
    # print(sys.modules)
    print("Cannot ${{{variable}}} {type}".format(
        variable="C:/work", type="End"))


def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))


ga = 12


class btest():
    bb = 88

    def __init__(self):
        self.ba = 112

    def btt(self):
        print('base test')


class ctest(btest):
    def __init__(self):
        super().__init__()
        self.a = ga
        super().btt()
        print(self.ba)

    def ttt(self):
        return self.a

    def btt(self):
        print('child test')


def ftest():
    print(ga)


import tempfile
import json


def my_obj_pairs_hook(lst):
    result = {}
    count = {}
    for key, val in lst:
        if key in count: count[key] = 1 + count[key]
        else: count[key] = 1
        if key in result:
            if count[key] > 2:
                result[key].append(val)
            else:
                result[key] = [result[key], val]
        else:
            result[key] = val
    return result

def super_call(f):
    def wrapper(self):
        getattr(super(type(self), self), f.__name__)()
        return f(self)

    return wrapper

class bb(object):
    pass

class base(bb):
    a = 123
    def __init__(self, data):
        self.data = data
        self.dd = {'a':1}

    def output(self):
        print('base data', self.data)


class derive(base):
    def __init_(self, data):
        super().__init__(data)

    @super_call
    def output(self):
        print('derive data', self.data)

from functools import wraps
 
def logit(logfile='out.log'):
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kw):
            log_string = func.__name__ + " was called"
            print(log_string)
            # 打开logfile，并写入内容
            with open(logfile, 'a') as opened_file:
                # 现在将日志打到指定的logfile
                opened_file.write(log_string + '\n')
            return func(*args, **kw)
        return wrapped_function
    return logging_decorator
            
 
@logit()
def myfunc1():
    pass

@logit('func2.log')
def myfunc2():
    pass

class Foo(object):
    def __init__(self, func):
        self._func = func

    def __call__(self):
        print ('class decorator runing')
        self._func()
        print ('class decorator ending')

@Foo
def bar():
    print ('bar')


import re
a =2

def test1():
    a = 3
    test()

def test():
    global a
    print(a)
if __name__ == '__main__':

    str = '松陵镇冬梅街199号万象汇花园1幢1013'
    str1 = '苏州吴中经济开发区郭巷街道尹山湖景花园50幢1903室'

    print(re.findall(r'\w+?(\d+)幢(\d+)', str1), re.I)


    dic = {'c':123,'b':45}

    ts = dic.setdefault('d',{})
    ts['aa'] = 111
    print(ts.setdefault('bb',123))
    print(dic, ts)
    print(sorted(dic.keys()))
    print(dic, ts)
