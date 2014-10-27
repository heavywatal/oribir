from PyQt4 import QtGui, QtCore
#import icons


class Quit(QtGui.QAction):
    def __init__(self, parent, app):
        super(Quit, self).__init__(parent)
        self.setText(self.tr("&Quit"))
        self.triggered.connect(app.quit)
        #self.triggered.connect(sys.exit)
#        self.setIcon(QtGui.QIcon(":system-shutdown"))
        qs = QtGui.QStyle.SP_TitleBarCloseButton
        self.setIcon(parent.style().standardIcon(qs))
        self.setShortcut('Ctrl+Q')
        self.setStatusTip(self.tr("Quit application"))


class Open(QtGui.QAction):
    def __init__(self, parent):
        super(Open, self).__init__(parent)
        self.setText(self.tr("&Open"))
#        self.setIcon(QtGui.QIcon(":document-open"))
        qs = QtGui.QStyle.SP_DialogOpenButton
        self.setIcon(parent.style().standardIcon(qs))
        self.setShortcut('Ctrl+O')


class Save(QtGui.QAction):
    def __init__(self, parent):
        super(Save, self).__init__(parent)
        self.setText(self.tr("&Save"))
#        self.setIcon(QtGui.QIcon(":document-save"))
        qs = QtGui.QStyle.SP_DialogSaveButton
        self.setIcon(parent.style().standardIcon(qs))
        self.setShortcut('Ctrl+S')


class About(QtGui.QAction):
    def __init__(self, parent):
        QtGui.QAction.__init__(self, parent)
        self.setText(self.tr("About"))
        qs = QtGui.QStyle.SP_MessageBoxInformation
        self.setIcon(parent.style().standardIcon(qs))
        self.triggered.connect(about)


def about(parent):
    return QtGui.QMessageBox.about(None,
            "About Origami Bird Simulator",
            "Takahiro Yamanoi and Watal M. Iwasaki")
