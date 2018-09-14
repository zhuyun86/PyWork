# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Desensitization.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SecKill(object):
    def setupUi(self, SecKill):
        SecKill.setObjectName("SecKill")
        SecKill.resize(510, 151)
        self.gridLayout = QtWidgets.QGridLayout(SecKill)
        self.gridLayout.setObjectName("gridLayout")

        ####login
        self.gp_login = QtWidgets.QGroupBox(SecKill)
        self.gp_login.setObjectName("gp_login")
        self.loginLayout = QtWidgets.QGridLayout(self.gp_login)
        self.loginLayout.setObjectName("loginLayout")
        self.lb_user_name = QtWidgets.QLabel(self.gp_login)
        self.lb_user_name.setScaledContents(True)
        self.lb_user_name.setObjectName("lb_user_name")
        self.le_user_name = QtWidgets.QLineEdit(self.gp_login)
        self.le_user_name.setObjectName("le_user_name")
        self.lb_password = QtWidgets.QLabel(self.gp_login)
        self.lb_password.setScaledContents(True)
        self.lb_password.setObjectName("lb_password")
        self.le_password = QtWidgets.QLineEdit(self.gp_login)
        self.le_password.setObjectName("le_password")
        self.le_password.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.pb_login = QtWidgets.QPushButton(self.gp_login)
        self.pb_login.setObjectName("pb_login")
        self.pb_login.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                    QtWidgets.QSizePolicy.Preferred)
        self.loginLayout.addWidget(self.lb_user_name, 0, 0)
        self.loginLayout.addWidget(self.le_user_name, 0, 1)
        self.loginLayout.addWidget(self.lb_password, 1, 0)
        self.loginLayout.addWidget(self.le_password, 1, 1)
        self.loginLayout.addWidget(self.pb_login, 0, 2, 2, 1)

        ###search
        self.gp_search = QtWidgets.QGroupBox(SecKill)
        self.gp_search.setObjectName("gp_search")
        self.searchLayout = QtWidgets.QGridLayout(self.gp_search)
        self.searchLayout.setObjectName("searchLayout")
        self.lb_goods = QtWidgets.QLabel(self.gp_search)
        self.lb_goods.setScaledContents(True)
        self.lb_goods.setObjectName("lb_goods")
        self.le_goods = QtWidgets.QLineEdit(self.gp_search)
        self.le_goods.setObjectName("le_goods")
        self.pb_search = QtWidgets.QPushButton(self.gp_search)
        self.pb_search.setObjectName("pb_search")
        self.tw_goods = QtWidgets.QTableWidget(self.gp_search)
        self.tw_goods.setMinimumHeight(240)
        header = ['time', 'price', 'name', 'url']
        self.tw_goods.setHorizontalHeaderLabels(header)
        self.tw_goods.setColumnCount(4)
        self.tw_goods.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.tw_goods.setSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                      QtWidgets.QSizePolicy.Expanding)
        self.searchLayout.addWidget(self.lb_goods, 0, 0)
        self.searchLayout.addWidget(self.le_goods, 0, 1)
        self.searchLayout.addWidget(self.pb_search, 0, 2)
        self.searchLayout.addWidget(self.tw_goods, 2, 0, 1, 3)

        ###seckill
        self.gp_seckill = QtWidgets.QGroupBox(SecKill)
        self.gp_seckill.setObjectName("gp_seckill")
        self.seckillLayout = QtWidgets.QGridLayout(self.gp_seckill)
        self.seckillLayout.setObjectName("seckillLayout")
        self.lb_url = QtWidgets.QLabel(self.gp_seckill)
        self.lb_url.setScaledContents(True)
        self.lb_url.setObjectName("lb_url")
        self.le_url = QtWidgets.QLineEdit(self.gp_seckill)
        self.le_url.setObjectName("le_url")
        self.lb_time = QtWidgets.QLabel(self.gp_seckill)
        self.lb_time.setScaledContents(True)
        self.lb_time.setObjectName("lb_time")
        self.le_time = QtWidgets.QLineEdit(self.gp_seckill)
        self.le_time.setObjectName("le_time")
        self.pb_seckill = QtWidgets.QPushButton(self.gp_seckill)
        self.pb_seckill.setObjectName("pb_seckill")
        self.pb_seckill.setSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                      QtWidgets.QSizePolicy.Preferred)
        self.seckillLayout.addWidget(self.lb_url, 0, 0)
        self.seckillLayout.addWidget(self.le_url, 0, 1)
        self.seckillLayout.addWidget(self.lb_time, 1, 0)
        self.seckillLayout.addWidget(self.le_time, 1, 1)
        self.seckillLayout.addWidget(self.pb_seckill, 0, 2, 2, 1)

        ###
        self.gridLayout.addWidget(self.gp_login, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.gp_search, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.gp_seckill, 2, 0, 1, 1)

        self.retranslateUi(SecKill)
        QtCore.QMetaObject.connectSlotsByName(SecKill)

    def retranslateUi(self, SecKill):
        _translate = QtCore.QCoreApplication.translate
        SecKill.setWindowTitle(_translate("SecKill", "JD SecKill"))
        self.gp_login.setTitle(_translate("SecKill", "*Login"))
        self.gp_search.setTitle(_translate("SecKill", "*Search"))
        self.gp_seckill.setTitle(_translate("SecKill", "*Seckill"))
        self.lb_user_name.setText(_translate("SecKill", "UserName:"))
        self.lb_password.setText(_translate("SecKill", "Password:"))
        self.pb_login.setText(_translate("SecKill", "Login"))
        self.lb_goods.setText(_translate("SecKill", "Goods:"))
        self.pb_search.setText(_translate("SecKill", "Search"))
        self.lb_url.setText(_translate("SecKill", "url:"))
        self.lb_time.setText(_translate("SecKill", "time:"))
        self.pb_seckill.setText(_translate("SecKill", "SecKill"))
