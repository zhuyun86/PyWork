# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Desensitization.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Desensitization(object):
    def setupUi(self, Desensitization):
        Desensitization.setObjectName("Desensitization")
        Desensitization.resize(510, 151)
        self.gridLayout = QtWidgets.QGridLayout(Desensitization)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(Desensitization)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lePath")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pbSelectFolder = QtWidgets.QPushButton(self.groupBox)
        self.pbSelectFolder.setObjectName("pbSelectFolder")
        self.horizontalLayout.addWidget(self.pbSelectFolder)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.pbDesensitize = QtWidgets.QPushButton(self.groupBox)
        self.pbDesensitize.setObjectName("pbDesensitize")
        self.verticalLayout.addWidget(self.pbDesensitize)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(Desensitization)
        QtCore.QMetaObject.connectSlotsByName(Desensitization)

    def retranslateUi(self, Desensitization):
        _translate = QtCore.QCoreApplication.translate
        Desensitization.setWindowTitle(_translate("Desensitization", "Desensitization"))
        self.groupBox.setTitle(_translate("Desensitization", "Desensitization"))
        self.label.setText(_translate("Desensitization", "Dicom Folder: "))
        self.pbSelectFolder.setText(_translate("Desensitization", "SelectFolder"))
        self.pbDesensitize.setText(_translate("Desensitization", "Desensitize"))

