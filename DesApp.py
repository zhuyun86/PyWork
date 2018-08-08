import sys, os
from DesUI import Ui_Desensitization
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5 import QtWidgets
import threading

import Desens

class DesForm(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.dicom_folder = os.getcwd()
        self.cv = threading.Condition()
        self.ui = Ui_Desensitization()
        self.ui.setupUi(self)

        self.ui.pbSelectFolder.clicked.connect(self.SelectFolder)
        self.ui.pbDesensitize.clicked.connect(self.Desensitize)

    def SelectFolder(self):
        dicom_folder = QFileDialog.getExistingDirectory(
            self, 'Open Dir', self.dicom_folder)
        if dicom_folder == '':
            return
        self.dicom_folder = str(dicom_folder)
        self.ui.lineEdit.setText(self.dicom_folder)
    
    def UpdateUI(self):
        with self.cv:
            self.ui.pbSelectFolder.setEnabled(False)
            self.ui.pbDesensitize.setEnabled(False)
            self.ui.pbDesensitize.setText('Desensitizing...')
            self.cv.wait()
            self.ui.pbSelectFolder.setEnabled(True)
            self.ui.pbDesensitize.setEnabled(True)
            self.ui.pbDesensitize.setText('Desensitize')
            print('UpdateUI:', threading.current_thread())

    def Desensitize(self):
        tt = threading.Thread(target=self.UpdateUI)
        tt.start()
        t = threading.Thread(target=Desens.DoDesens, args=(self.dicom_folder, self.cv))
        t.start()
        print('UI:', threading.current_thread())

        
        # Desens.TravDir(self.dicom_folder)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = DesForm()
    Form.show()
    sys.exit(app.exec_())
