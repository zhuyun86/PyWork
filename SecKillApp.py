import sys, os, re
from SecKillUI import Ui_SecKill
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5 import QtWidgets

from SecKill import CSecKill

from datetime import datetime, timedelta


class SecKillForm(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_SecKill()
        self.ui.setupUi(self)
        self.timer_id = None

        self.__seckill = None

        self.ui.pb_login.clicked.connect(self.Login)
        self.ui.pb_search.clicked.connect(self.SearchGoods)
        self.ui.tw_goods.itemClicked.connect(self.ItemClicked)
        self.ui.pb_seckill.clicked.connect(self.KillGoods)

    def getSeckill(self):
        if not self.__seckill:
            self.__seckill = CSecKill()
        return self.__seckill

    def Login(self):
        user_name = self.ui.le_user_name.text()
        password = self.ui.le_password.text()
        if not (user_name and password):
            return

        try:
            url = 'https://www.jd.com'
            seckill = self.getSeckill()
            seckill.Login(url, user_name, password)
        except BaseException as e:
            print('Error:', e)

    def SearchGoods(self):
        goods_name = self.ui.le_goods.text()
        if not (goods_name):
            return

        try:
            urls = []
            seckill = self.getSeckill()
            seckill.SearchGoods(goods_name, urls)
            self.ui.tw_goods.clear()
            for index, url in enumerate(urls):
                self.ui.tw_goods.insertRow(index)
                tw_item = [
                    QtWidgets.QTableWidgetItem(),
                    QtWidgets.QTableWidgetItem(),
                    QtWidgets.QTableWidgetItem(),
                    QtWidgets.QTableWidgetItem()
                ]
                for i in range(4):
                    tw_item[i].setText(url[i])
                    self.ui.tw_goods.setItem(index, i, tw_item[i])
        except BaseException as e:
            print('Error:', e)

    def ItemClicked(self, item):
        self.ui.le_url.setText(self.ui.tw_goods.item(item.row(), 3).text())
        self.ui.le_time.setText(self.ui.tw_goods.item(item.row(), 0).text())

    def KillGoods(self):
        try:
            seckill = self.getSeckill()
            kill_time, countdown_time = seckill.GetCountdown()
            print('killgoods', kill_time, countdown_time)
            cd = countdown_time.split(':')
            delta = timedelta(0, int(cd[2]), 0, 0, int(cd[1]), int(cd[0]))
        except BaseException as e:
            print('Error:', e)

        le_url = self.ui.le_url.text()
        le_time = self.ui.le_time.text()

        now_y = kill_time.year
        now_m = kill_time.month
        now_d = kill_time.day
        parts = re.findall(r'(\D*?)(\d+):(\d+)', le_time)

        set_time = datetime(now_y, now_m, (now_d + 1
                                           if parts[0][0] else now_d),
                            int(parts[0][1]), int(parts[0][2]))

        delta += set_time - kill_time
        if self.timer_id:
            self.killTimer(self.timer_id)
            self.timer_id = None
        self.timer_id = self.startTimer(delta.seconds * 1000)
        print(delta, delta.seconds)

        if not (le_url and le_time):
            return
        try:
            seckill.KillGoods(le_url, le_time)
        except BaseException as e:
            print('Error:', e)

    def timerEvent(self, evt):
        if evt.timerId() == self.timer_id:
            print('order')
            seckill = self.getSeckill()
            seckill.OrderSubmit()
            self.killTimer(self.timer_id)
            self.timer_id = None
            print('submit!')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = SecKillForm()
    Form.show()
    sys.exit(app.exec_())
