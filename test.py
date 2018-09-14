from pyhocon import ConfigFactory
from datetime import datetime
import re

from collections import OrderedDict
if __name__ == '__main__':
    start_time = '明日19:35'


    now_time = datetime.now()
    now_y = now_time.year
    now_m = now_time.month
    now_d = now_time.day
    parts = re.findall(r'(\D*?)(\d+):(\d+)', start_time)
    print(parts)
    

    kill_time = datetime(now_y, now_m, (now_d+1 if parts[0][0] else now_d) , int(parts[0][1]), int(parts[0][2]))
    print(kill_time)

    pri = '￥888.090'
    fp = re.findall(r'\d+.\d+', pri)
    print(fp)