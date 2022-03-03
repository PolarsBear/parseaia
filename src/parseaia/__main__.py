import sys
from .main import Project
from .uiclasses import Component
from .codeclasses import Block

from PyQt5 import QtCore, QtGui, QtWidgets


def has_proper_str(obj):
    return type(obj).__str__ is not object.__str__


class SimpleTextAsset:
    text: str

    def __init__(self, text):
        self.text = text


class UIMainWindow(object):
    def setup_ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(746, 598)
        MainWindow.setStyleSheet("border-color: rgb(0, 0, 0);\n"
                                 "border-width: 5px;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.screensBox = QtWidgets.QGroupBox(self.centralwidget)
        self.screensBox.setGeometry(QtCore.QRect(9, 9, 161, 201))
        self.screensBox.setObjectName("screensBox")
        self.screens = QtGui.QStandardItemModel()
        self.screensview = QtWidgets.QListView(self.screensBox)
        self.screensview.setGeometry(QtCore.QRect(0, 20, 161, 181))
        self.screensview.setObjectName("screens")
        self.screensview.setModel(self.screens)
        self.screensview.setEditTriggers(QtWidgets.QListView.NoEditTriggers)
        self.screensview.clicked.connect(self.screen_item_selected)
        self.UIBox = QtWidgets.QGroupBox(self.centralwidget)
        self.UIBox.setGeometry(QtCore.QRect(10, 220, 351, 331))
        self.UIBox.setObjectName("UIBox")
        self.UIElements = QtGui.QStandardItemModel()
        self.UITree = QtWidgets.QTreeView(self.UIBox)
        self.UITree.setGeometry(QtCore.QRect(0, 20, 351, 311))
        self.UITree.setObjectName("UITree")
        self.UITree.setEditTriggers(QtWidgets.QTreeView.NoEditTriggers)
        self.UITree.setModel(self.UIElements)
        self.codeBox = QtWidgets.QGroupBox(self.centralwidget)
        self.codeBox.setGeometry(QtCore.QRect(380, 220, 351, 331))
        self.codeBox.setObjectName("codeBox")
        self.codeElements = QtGui.QStandardItemModel()
        self.codeTree = QtWidgets.QTreeView(self.codeBox)
        self.codeTree.setGeometry(QtCore.QRect(0, 20, 351, 311))
        self.codeTree.setObjectName("codeTree")
        self.codeTree.setEditTriggers(QtWidgets.QTreeView.NoEditTriggers)
        self.codeTree.setModel(self.codeElements)
        self.assetsBox = QtWidgets.QGroupBox(self.centralwidget)
        self.assetsBox.setGeometry(QtCore.QRect(180, 10, 161, 201))
        self.assetsBox.setObjectName("assetsBox")
        self.assets = QtGui.QStandardItemModel()
        self.assetsview = QtWidgets.QListView(self.assetsBox)
        self.assetsview.setGeometry(QtCore.QRect(0, 20, 161, 181))
        self.assetsview.setObjectName("assets")
        self.assetsview.setModel(self.assets)
        self.assetsview.setEditTriggers(QtWidgets.QListView.NoEditTriggers)
        self.assetsview.clicked.connect(self.asset_item_selected)
        self.propBox = QtWidgets.QGroupBox(self.centralwidget)
        self.propBox.setGeometry(QtCore.QRect(380, 10, 161, 201))
        self.propBox.setObjectName("propBox")
        self.properties = QtGui.QStandardItemModel()
        self.props = QtWidgets.QListView(self.propBox)
        self.props.setGeometry(QtCore.QRect(0, 20, 161, 181))
        self.props.setObjectName("props")
        self.props.setModel(self.properties)
        self.props.setEditTriggers(QtWidgets.QListView.NoEditTriggers)
        self.props.clicked.connect(self.props_item_selected)
        self.valueBox = QtWidgets.QGroupBox(self.centralwidget)
        self.valueBox.setGeometry(QtCore.QRect(550, 10, 181, 201))
        self.valueBox.setObjectName("valueBox")
        self.value = QtWidgets.QLabel(self.valueBox)
        self.value.setGeometry(QtCore.QRect(0, 20, 181, 181))
        self.value.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.value.setWordWrap(True)
        self.value.setText("")
        self.value.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.value.setObjectName("value")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 746, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.file_opener = QtWidgets.QFileDialog(MainWindow)
        self.file_opener.setAcceptMode(self.file_opener.AcceptOpen)
        self.file_opener.fileSelected.connect(self.open_file)
        self.actionOpen.triggered.connect(self.file_opener.open)
        self.menuFile.addAction(self.actionOpen)
        self.menubar.addAction(self.menuFile.menuAction())
        self.selected_item = None

        self.retranslate_ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def process_UI_Element(self,element:Component, column: list, parent):
        column.append(element)
        item = QtGui.QStandardItem(element.Name + f": {element.Type}")
        parent.appendRow(item)

        if hasattr(element,"Components"):
            c = []
            self.UIlist.append(c)
            for i in element.Components:
                self.process_UI_Element(i,c,item)


    """def process_code_element(self, element:Block, column:list, parent):
        column.append(element)
        item = QtGui.QStandardItem(element.type)
        parent.appendRow(item)

        if element.statements.__len__() > 0 or element.fields.__len__() > 0 or element.next is not None:
            c = []

        if element.statements.__len__() > 0:
            statement_item = QtGui.QStandardItem("statements")
            item.appendRow(statement_item)
            for i in element.statements:
                print(i.next,i.child.value.__dict__)
                tmp = QtGui.QStandardItem(i.name)
                statement_item.appendRow(tmp)
                tmp2 = QtGui.QStandardItem(i.child.type)
                tmp.appendRow(tmp2)

        if element.fields.__len__() > 0:
            fields_item = QtGui.QStandardItem("fields")
            item.appendRow(fields_item)

        if hasattr(element,"next"):
            self.process_code_element(element.next,c,item)"""



    def screen_item_selected(self, item: QtCore.QModelIndex):
        self.selected_item = self.screenlist[item.row()]
        self.display_props(self.selected_item)

        self.UIlist = []
        self.UIElements.clear()
        for i in self.selected_item.UI.Properties.Components:
            self.process_UI_Element(i,self.UIlist,self.UIElements)

        self.codelist = []
        self.codeElements.clear()
        self.codeElements.appendRow(QtGui.QStandardItem("Coming Soon"))
        """for i in self.selected_item.Code.blocks:
            self.process_code_element(i,self.codelist,self.codeElements)"""


    def props_item_selected(self, item: QtCore.QModelIndex):
        tmp: object = self.propertylist[item.row()]
        if has_proper_str(tmp) or not hasattr(tmp, "__dict__"):
            self.value.setText(str(tmp))
        else:
            self.selected_item = tmp
            self.display_props(self.selected_item)


    def asset_item_selected(self,item: QtCore.QModelIndex):
        self.selected_item = self.assetlist[item.row()]
        self.display_props(self.selected_item)

    def display_props(self, object):
        self.propertylist = []
        self.properties.clear()
        for k, v in object.__dict__.items():
            self.propertylist.append(v)
            self.properties.appendRow(QtGui.QStandardItem(f"{k}: {type(v).__name__}"))

    def open_file(self, path):
        self.project = Project(path)
        self.assets.clear()
        self.screens.clear()
        self.screenlist = []
        self.assetlist = []

        for i in self.project.screens:
            self.screenlist.append(i)
            self.screens.appendRow(QtGui.QStandardItem(i.UI.Properties.Name))

        for i in self.project.images:
            self.assetlist.append(i)
            self.assets.appendRow(QtGui.QStandardItem(i.filename))

        for i in self.project.audio:
            self.assetlist.append(i)
            self.assets.appendRow(QtGui.QStandardItem(i.filename))

        for i in self.project.assets:
            self.assetlist.append(SimpleTextAsset(self.project.assets[i]))
            self.assets.appendRow(QtGui.QStandardItem(i))

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ParseAIA"))
        self.screensBox.setTitle(_translate("MainWindow", "Screens"))
        self.UIBox.setTitle(_translate("MainWindow", "UI"))
        self.codeBox.setTitle(_translate("MainWindow", "Code"))
        self.assetsBox.setTitle(_translate("MainWindow", "Assets"))
        self.propBox.setTitle(_translate("MainWindow", "Properties"))
        self.valueBox.setTitle(_translate("MainWindow", "Value"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = UIMainWindow()
        self.ui.setup_ui(self)


def main():
    app = QtWidgets.QApplication([])
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
