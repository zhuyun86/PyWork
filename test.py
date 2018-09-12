from pyhocon import ConfigFactory
import os

from collections import OrderedDict
if __name__ == '__main__':
   parser = ConfigFactory.parse_file('test.conf')
   print(type(parser.get('databases.mysql.username', 'default')))
   print(parser.get('databases.active'),type(parser.get('databases.active')))
   print(parser.get('databases.home_dir', 'default'))
   print(parser['large-jvm-opts'])
   print(parser['aa'],type(parser['aa']),dict(parser['aa']))

