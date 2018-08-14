import sys, os
from CompressUI import Ui_CompressTool
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5 import QtWidgets
import threading

import CompressTool


class DesForm(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.nii_dir = os.getcwd()
        self.gz_dir = os.getcwd()
        self.cv = threading.Condition()
        self.ui = Ui_CompressTool()
        self.ui.setupUi(self)
        self.ui.lineEdit.setText(self.nii_dir)
        self.ui.lineEdit1.setText(self.gz_dir)

        self.ui.pbSelectFolder.clicked.connect(self.SelectFolder)
        self.ui.pbSelectCompressFolder.clicked.connect(
            self.SelectCompressFolder)
        self.ui.pbCompressNii.clicked.connect(self.CompressNii)
        self.ui.pbDecompressNii.clicked.connect(self.DecompressNii)

    def SelectFolder(self):
        nii_dir = QFileDialog.getExistingDirectory(self, 'Open Dir',
                                                   self.nii_dir)
        if nii_dir == '':
            return
        self.nii_dir = str(nii_dir)
        self.ui.lineEdit.setText(self.nii_dir)

    def SelectCompressFolder(self):
        gz_dir = QFileDialog.getExistingDirectory(self, 'Open Dir',
                                                  self.gz_dir)
        if gz_dir == '':
            return
        self.gz_dir = str(gz_dir)
        self.ui.lineEdit1.setText(self.gz_dir)

    def UpdateUI(self):
        with self.cv:
            self.ui.pbCompressNii.setEnabled(False)
            self.ui.pbDecompressNii.setEnabled(False)
            self.cv.wait()
            self.ui.pbCompressNii.setEnabled(True)
            self.ui.pbDecompressNii.setEnabled(True)

    def CompressNii(self):
        if not (self.nii_dir and self.gz_dir):
            QMessageBox.warning(None, 'Warning', '选择nii目录和压缩目录')
            return

        tt = threading.Thread(target=self.UpdateUI)
        tt.start()
        t = threading.Thread(
            target=CompressTool.CompressNii,
            args=(self.nii_dir, self.gz_dir, self.cv))
        t.start()

    def DecompressNii(self):
        if not (self.nii_dir and self.gz_dir):
            QMessageBox.warning(None, 'Warning', '选择nii目录和压缩目录')
            return

        tt = threading.Thread(target=self.UpdateUI)
        tt.start()
        t = threading.Thread(
            target=CompressTool.DecompressNii,
            args=(self.gz_dir, self.nii_dir, self.cv))
        t.start()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = DesForm()
    Form.show()
    sys.exit(app.exec_())
