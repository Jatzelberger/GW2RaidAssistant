import ctypes
import sys
from resources.uix.windowLoading import WindowLoading
from PyQt6.QtWidgets import QApplication


if __name__ == '__main__':

    myAppID = 'jatzelbergerinc.raidhelper.mainwindow.vfour'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppID)

    app = QApplication(sys.argv)
    window = WindowLoading()
    window.show()
    app.exec()
