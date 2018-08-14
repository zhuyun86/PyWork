# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CompressTool(object):
    def setupUi(self, CompressTool):
        CompressTool.setObjectName("CompressTool")
        CompressTool.resize(510, 151)
        self.gridLayout = QtWidgets.QGridLayout(CompressTool)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(CompressTool)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")

        self.gLayout = QtWidgets.QGridLayout()
        self.gLayout.setObjectName("gLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.gLayout.addWidget(self.label, 0, 0)
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lePath")
        self.gLayout.addWidget(self.lineEdit, 0, 1)
        self.pbSelectFolder = QtWidgets.QPushButton(self.groupBox)
        self.pbSelectFolder.setObjectName("pbSelectFolder")
        self.gLayout.addWidget(self.pbSelectFolder, 0, 2)

        self.label1 = QtWidgets.QLabel(self.groupBox)
        self.label1.setScaledContents(True)
        self.label1.setObjectName("label1")
        self.gLayout.addWidget(self.label1, 1, 0)
        self.lineEdit1 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit1.setReadOnly(True)
        self.lineEdit1.setObjectName("lePath1")
        self.gLayout.addWidget(self.lineEdit1, 1, 1)
        self.pbSelectCompressFolder = QtWidgets.QPushButton(self.groupBox)
        self.pbSelectCompressFolder.setObjectName("pbSelectCompressFolder")
        self.gLayout.addWidget(self.pbSelectCompressFolder, 1, 2)
        self.verticalLayout.addLayout(self.gLayout)

        self.pbCompressNii = QtWidgets.QPushButton(self.groupBox)
        self.pbCompressNii.setObjectName("pbCompressNii")
        self.verticalLayout.addWidget(self.pbCompressNii)
        self.pbDecompressNii = QtWidgets.QPushButton(self.groupBox)
        self.pbDecompressNii.setObjectName("pbDecompressNii")
        self.verticalLayout.addWidget(self.pbDecompressNii)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(CompressTool)
        QtCore.QMetaObject.connectSlotsByName(CompressTool)

    def retranslateUi(self, Desensitization):
        _translate = QtCore.QCoreApplication.translate
        Desensitization.setWindowTitle(
            _translate("CompressTool", "CompressTool"))
        self.groupBox.setTitle(_translate("CompressTool", "CompressTool"))
        self.label.setText(_translate("CompressTool", "nii Folder: "))
        self.label1.setText(_translate("CompressTool", "gz Folder: "))
        self.pbSelectFolder.setText(_translate("CompressTool", "Select..."))
        self.pbSelectCompressFolder.setText(
            _translate("CompressTool", "Select..."))
        self.pbCompressNii.setText(_translate("CompressTool", "CompressNii"))
        self.pbDecompressNii.setText(
            _translate("CompressTool", "DecompressNii"))
