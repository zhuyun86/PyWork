import sys
import os, time, random
from multiprocessing import Process
from ztest import tet
import base64
import struct

a = 2
b = 2


def test():
    # _test()
    s = b'\x42\x4d\x38\x8c\x0a\x00\x00\x00\x00\x00\x36\x00\x00\x00\x28\x00\x00\x00\x80\x02\x00\x00\x68\x01\x00\x00\x01\x00\x18\x00'
    print(struct.unpack('<ccIIIIIIHH', s))
    # tet()
    return

    beg = time.time()
    time.sleep(random.random() * 10)
    end = time.time()
    print("Time is {}".format(end - beg))


def _test():
    __test()


def __test():
    print("{2}{0}{1}".format(1, "fdd", 1.2323))
    # print(sys.modules)
    print("Cannot ${{{variable}}} {type}".format(
        variable="C:/work", type="End"))


def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))


if __name__ == '__main__':
    test()
else:
    print('Parent pid {}'.format(os.getpid()))
    p = Process(target=run_proc, args=('test', ))
    p.start()
    p.join()
    print('Child process end.')