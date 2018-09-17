import sys
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi


class TestLoadUI(QDialog):
    def __init__(self, *args):
        super(TestLoadUI, self).__init__(*args)
        loadUi('Desensitization.ui', self)
        self.pbDesensitize.clicked.connect(self.BtnClicked)

    def BtnClicked(self):
        print('clicked')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Form = TestLoadUI()
    Form.show()
    sys.exit(app.exec_())
