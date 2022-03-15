
#!python3
# encoding:utf-8
import ctypes
import ctypes.wintypes
from queue import Empty
from traceback import print_last
import win32gui

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

user32 = ctypes.windll.user32        
# https://docs.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
DWMWA_EXTENDED_FRAME_BOUNDS = 9

class Window(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #ウィンドウ背景の透明化オプション
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #タスクバーに表示されない/タイトルバーの削除/常に画面の前面にある
        self.setWindowFlags(QtCore.Qt.Tool|QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint)
        #ウィンドウハンドルをメモ帳に指定
        self.handle = self.__get_handle("masterduel")
        self.flag = 1
        global button_open
        global rect
        if self.handle:
            rect = ctypes.wintypes.RECT()
            ctypes.windll.dwmapi.DwmGetWindowAttribute(self.handle, DWMWA_EXTENDED_FRAME_BOUNDS, ctypes.pointer(rect), ctypes.sizeof(rect))
            self.setGeometry(rect.left, rect.bottom/2, 50, 50)
        
        #ボタン
        button_open =  QtWidgets.QPushButton("", self)
        button_open.setStyleSheet("color: rgba(225, 0, 0, 225);")
        button_open.clicked.connect(self.open_window)
        button_open.move(0, 0)
        button_open.resize(30, 30)

        #スライダ用レイアウトの作成
        self.sliderBox = QtWidgets.QHBoxLayout()
        self.sliderBox.setGeometry(QtCore.QRect(0, rect.bottom, rect.right - rect.left/3, 30))
        self.setLayout(self.sliderBox)

        self.installEventFilter(self)
        self.setStyleSheet("background-color: rgba(170, 170, 170, 128);")

        self.layersize = 0

    def valueChangedCallback(self, value):
        # 「sender」を使って、どのウィジェットから呼び出されたか調べる。
        sender = self.sender()
         
        # QSpinBoxが変更された場合
        if sender == self.spinbox:
            # QSliderのシグナルが発生しないようにブロックする
            self.slider.blockSignals(True)
             
            # QSliderの値を変更する
            self.slider.setValue(value)
             
            # QSliderのシグナルが発生するように戻す
            self.slider.blockSignals(False)
         
        # QSliderが変更された場合
        elif sender == self.slider:
            # QSpinBoxのシグナルが発生しないようにブロックする
            self.spinbox.blockSignals(True)
             
            # QSpinBoxの値を変更する
            self.spinbox.setValue(value)
             
            # QSpinBoxのシグナルが発生するように戻す
            self.spinbox.blockSignals(False)
        self.layersize = value

    #ウィンドウを開閉
    def open_window(self):
        if self.flag == 1: #開く
            print("open")
            self.setGeometry(rect.left, rect.top, (rect.right - rect.left)/3, rect.bottom - rect.top)
            self.flag = 0
            #spinbox
            self.spinbox = QtWidgets.QSpinBox(self)
            self.spinbox.setGeometry(0, 0, 50, 30)
            self.sliderBox.insertWidget(-1, self.spinbox)
            self.spinbox.valueChanged[int].connect(self.valueChangedCallback)   
            #スライダ
            self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
            self.slider.setGeometry(0, 0, (rect.right - rect.left)/3 - 100, 30)
            self.sliderBox.insertWidget(-1, self.slider)
            self.slider.valueChanged[int].connect(self.valueChangedCallback)
        elif self.flag == 0: #閉じる
            print("close")
            self.slider.deleteLater()
            self.spinbox.deleteLater()
            self.setGeometry(rect.left, rect.bottom/2 , 50 + self.layersize, 50 + self.layersize)
            self.flag = 1

    #ウィンドウを閉じたとき
    # def close_window(self):

    @staticmethod
    #ウィンドウハンドルを返す
    def __get_handle(process_name):        
        return user32.FindWindowW(0, process_name)
    
    #トップレベルのWidgetはWA_TranslucentBackgroundフラグが立つと、
    # 背景が描画されなくなるので、paintEvent側で描画する。
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(0, 0, self.width(), self.height(), painter.background())

#タスクトレーに表示する
class TaskTray_Icon(QtWidgets.QSystemTrayIcon):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        menu = QtWidgets.QMenu()
        #終了ボタンの追加
        quit_action = menu.addAction("Quit")
        quit_action.triggered.connect(self.__quit)

        self.setContextMenu(menu)
        #アイコンの設定(赤単色)
        pixmap = QtGui.QPixmap(QtCore.QSize(32, 32))
        pixmap.fill(QtGui.QColor("red"))
        icon = QtGui.QIcon(pixmap)

        self.setIcon(icon)

    def __quit(self):
        QtWidgets.QApplication.quit()


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    #トレイアイコンを生成して表示
    trayicon = TaskTray_Icon()
    trayicon.show()

    window = Window()
    window.show()

    exit_code = app.exec_()
    exit(exit_code)