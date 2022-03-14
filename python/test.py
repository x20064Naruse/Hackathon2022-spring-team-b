#!python3
# encoding:utf-8

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

class Window(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowFlags(QtCore.Qt.Tool|QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint)

        # 撮影用に位置を変更
        self.setGeometry(1400, 850, 200, 200)

        label = QtWidgets.QLabel("Frame Less Window Sample", self)
        label.setGeometry(0, 0, 200, 200)
        label.setStyleSheet("background-color: #222; color: #EEE;")

class TaskTray_Icon(QtWidgets.QSystemTrayIcon):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        menu = QtWidgets.QMenu()

        quit_action = menu.addAction("Quit")
        quit_action.triggered.connect(self.__quit)

        # コンテキストメニューに作成したメニューをセット
        self.setContextMenu(menu)

        # NOTE: アイコンには通常はpngなどを指定するが、
        # サンプルなのでPixmapでもモックを作ってお茶を濁す。
        # icon = QtGui.QIcon('icon.png')
        pixmap = QtGui.QPixmap(QtCore.QSize(32, 32))
        pixmap.fill(QtGui.QColor("red"))
        icon = QtGui.QIcon(pixmap)

        self.setIcon(icon)

    def __quit(self):
        QtWidgets.QApplication.quit()


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    # トレイアイコンを生成して表示。
    trayicon = TaskTray_Icon()

    trayicon.show()

    window = Window()
    window.show()
    exit(app.exec_())