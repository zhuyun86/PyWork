import requests
from bs4 import BeautifulSoup
import json
import sqlite3
import re


class HttpPost:
    def __init__(self):
        self.url = 'http://spf.szfcweb.com/szfcweb/(S(uoruobeqvf4unje1cdbykr55))/DataSerach/CanSaleHouseSelectIndex.aspx'
        self.data = None
        self.header = {
            'User-Agent':
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        }
        self.conn = sqlite3.connect('test.db')
        self.cursor = self.conn.cursor()

        self.ReadData()

        for n in range(16):
            self.PostData(n)

        self.cursor.close()
        self.conn.commit()
        self.conn.close()

    def PostData(self, index = 0):
        print(index)
        self.data["ctl00$MainContent$PageGridView1$ctl22$PageList"] = index
        response = requests.post(self.url, data=self.data, headers=self.header)
        response.encoding = 'utf-8'
        # with open('zzzzzzzzz.html', 'w') as fw:
        #     fw.write(response.text)

        bs = BeautifulSoup(response.text, 'lxml')

        table = bs.find('table', id='ctl00_MainContent_PageGridView1')

        #txt
        with open('zzzzzzzzz.txt', 'a') as f:
            for th in table.tr.find_all('th'):
                f.write(th.text)
                f.write('\t')
            f.write('\n')

            for index in table.find_all('tr'):
                for td in index.find_all('td'):
                    f.write(td.text)
                    f.write('\t')
                f.write('\n')

        ##db
        # rec = []
        # for tr in table.find_all('tr'):
        #     rec.clear()
        #     for td in tr.find_all('td'):
        #         rec.append(td.text)
        #     if len(rec)<6:
        #         continue
        #     self.cursor.execute('insert into houseinfo(addr,name,type,size,area,unit_price)\
        #      values("{}","{}","{}","{}",{},{})'\
        #      .format(rec[0],rec[1],rec[2],rec[3],float(rec[4]),float(rec[5])))
        # self.conn.commit()

        ##db
        rec = []
        for tr in table.find_all('tr'):
            rec.clear()
            for td in tr.find_all('td'):
                rec.append(td.text)
            if len(rec) < 6:
                continue

            pattern = re.compile(r'\d+')
            numbers = pattern.findall(rec[0])
            if len(numbers) < 2:
                continue
            self.cursor.execute('insert into house(building,room,size,area,price)\
             values("{:0>2}","{:0>4}","{}",{},{})'\
             .format(numbers[-2],numbers[-1],rec[3],float(rec[4]),float(rec[5])))
        self.conn.commit()

    def ReadData(self):
        with open('data.json', 'r') as file:
            jf = json.load(file)
            self.data = jf


if __name__ == '__main__':

    hp = HttpPost()
