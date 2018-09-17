import sys, os
from SecKillUI import Ui_SecKill
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5 import QtWidgets

from SecKill import CSecKill

from datetime import timedelta


class SecKillForm(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_SecKill()
        self.ui.setupUi(self)
        self.timer_id = 0

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

        self.timer_id = self.startTimer(delta.seconds)

        le_url = self.ui.le_url.text()
        le_time = self.ui.le_time.text()
        if not (le_url and le_time):
            return
        try:
            seckill.KillGoods(le_url, le_time)
        except BaseException as e:
            print('Error:', e)

    def timerEvent(self, evt):
        if evt.timerId() == self.timer_id:
            self.killTimer(self.timer_id)
            print('timer:', evt.timerId())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = SecKillForm()
    Form.show()
    sys.exit(app.exec_())
