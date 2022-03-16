
#!python3
# encoding:utf-8
import ctypes
import ctypes.wintypes
from queue import Empty
from traceback import print_last
import datetime

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
        self.onetimeFlag = 0
        self.layersize = 0
        self.comboid = 1
        self.watchsizew = 50
        self.watchsizeh = 50
        self.nextschedule_h = "23"
        self.nextschedule_m = "0"
        self.remainmin = "x"
        global rect
        if self.handle:
            rect = ctypes.wintypes.RECT()
            ctypes.windll.dwmapi.DwmGetWindowAttribute(self.handle, DWMWA_EXTENDED_FRAME_BOUNDS, ctypes.pointer(rect), ctypes.sizeof(rect))
            self.setGeometry(rect.left, rect.bottom/2, 50, 60)
            self.setStyleSheet("background-color: rgba(170, 170, 170, 0);")
        # ボタン
        global button_open
        button_open =  QtWidgets.QPushButton("", self)
        button_open.clicked.connect(self.open_window)
        button_open.setStyleSheet("background-color: rgba(170, 170, 170, 225);")
        button_open.move(0, 0)
        button_open.resize(15, 15)
        #スクロール用レイアウト
        self.scrollBox = QtWidgets.QVBoxLayout()
        self.scrollBox.setContentsMargins(0, 0, 0, 0)
        # 残りのウィジェット用レイアウトの作成
        self.openBox = QtWidgets.QVBoxLayout()
        self.openBox.setContentsMargins(0, 0, 0, 0)
        # 残り時間レイアウトの作成
        self.timerBox = QtWidgets.QHBoxLayout()
        self.timerBox.setContentsMargins(0, 0, 0, 0)
        # 残り時間
        self.label = QtWidgets.QLabel(self.remainmin + "分")
        self.label.setStyleSheet("background-color: rgba(0, 0, 0, 128); color: rgba(170, 170, 170, 255);font-family: impact;font-size:27px;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.timerBox.setContentsMargins(0, 0, 0, 0)
        self.timerBox.addWidget(self.label)
        # 時計用レイアウトの作成
        self.clockBox = QtWidgets.QHBoxLayout()
        self.clockBox.setContentsMargins(0, 0, 0, 0)
        # 時計
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.setcurrenttime)
        self.timedisplay = QtWidgets.QLCDNumber(self)
        self.timedisplay.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.timedisplay.setDigitCount(8)
        self.timedisplay.setGeometry(0 , 0, 50, 50)
        self.clockBox.setContentsMargins(0, 0, 0, 0)
        self.setcurrenttime()
        timer.start(10)
        self.timedisplay.setStyleSheet("background-color: rgba(0, 0, 0, 128); color: rgba(225, 225, 225, 225);font-size:106px;")
        self.clockBox.addWidget(self.timedisplay)
        # 親レイアウトの作成
        self.centralwidgetLayout = QtWidgets.QVBoxLayout()
        self.centralwidgetLayout.setContentsMargins(0, 15, 0, 0)
        self.centralwidgetLayout.addLayout(self.clockBox, 2)
        self.centralwidgetLayout.addLayout(self.timerBox, 1)
        self.centralwidgetLayout.addLayout(self.scrollBox, 3)
        self.centralwidgetLayout.addLayout(self.openBox, 13)
        self.setLayout(self.centralwidgetLayout)

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
            button_open.move(0, 0)
            if self.onetimeFlag != 0:
                self.strechBox.deleteLater()
            print("open")
            self.flag = 0
            self.setGeometry(rect.left, rect.top, (rect.right - rect.left)/3, rect.bottom - rect.top)
            self.setStyleSheet("background-color: rgba(170, 170, 170, 225);")
            #時計
            self.clockBox.setContentsMargins(0, 0, 0, 0)
            # 残り時間
            # self.label.setText(self.nextschedule_h + ":" + self.nextschedule_m + "まで残り" + self.remainmin + "分")
            # self.label.setStyleSheet("background-color: rgba(0, 0, 0, 128); color: rgba(170, 170, 170, 255);font-family: impact;font-size:81px;")
            # scroll
            self.scrollArea = QtWidgets.QScrollArea(self)
            self.scrollArea.setWidgetResizable(True)
            self.scrollAreaWidget = QtWidgets.QWidget()
            self.scrollAreaWidgetLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidget)
            self.scrollArea.setWidget(self.scrollAreaWidget)
            self.scrollBox.insertWidget(0, self.scrollArea, 1)
            self.addtask()
            self.addtask()
            self.addtask()
            self.addtask()
            self.addtask()
            self.addtask()
            self.addtask()
            self.openBox.addStretch()
            # コンボボックス用レイアウト
            self.layerpos = QtWidgets.QHBoxLayout()
            # comboBox
            self.comboBox = QtWidgets.QComboBox()
            self.comboBox.addItems(['左上', '左中', '左下', '右上', '右中', '右下'])
            self.layerpos.insertWidget(-1, self.comboBox)
            self.comboBox.setCurrentIndex(self.comboid)
            self.openBox.insertLayout(-1, self.layerpos, 1)
            # スライダ用レイアウトの作成
            self.sliderBox = QtWidgets.QHBoxLayout()
            # spinbox
            self.spinbox = QtWidgets.QSpinBox(self)
            self.spinbox.setGeometry(0, 0, 50, 30)
            self.sliderBox.insertWidget(-1, self.spinbox, 1)
            self.spinbox.setValue(self.layersize)
            self.spinbox.valueChanged[int].connect(self.valueChangedCallback)   
            # スライダ
            self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
            self.slider.setGeometry(0, 0, (rect.right - rect.left)/3 - 100, 30)
            self.sliderBox.insertWidget(-1, self.slider, 9)
            self.slider.setValue(self.layersize)
            self.slider.valueChanged[int].connect(self.valueChangedCallback)
            self.openBox.insertLayout(-1, self.sliderBox, 1)
            self.onetimeFlag = 1

        elif self.flag == 0: #閉じる
            print("close")
            self.comboid = self.comboBox.currentIndex()
            self.scrollArea.deleteLater()
            self.sliderBox.deleteLater()
            self.slider.deleteLater()
            self.spinbox.deleteLater()
            self.comboBox.deleteLater()

            self.setStyleSheet("background-color: rgba(170, 170, 170, 0);")
            # self.label.setText(self.remainmin + "分")
            # self.label.setStyleSheet("background-color: rgba(0, 0, 0, 128); color: rgba(170, 170, 170, 255);font-family: impact;font-size:27px;")
            # self.label.setAlignment(QtCore.Qt.AlignCenter)

            if self.comboid == 0:
                self.setGeometry(rect.left, rect.top , 50 + 1.5*self.layersize, 50 + 1*self.layersize)
                button_open.move(0, 0)
            elif self.comboid == 1:
                self.setGeometry(rect.left, rect.bottom/2, 50 + 1.5*self.layersize, 50 + 1.5*self.layersize)
                button_open.move(0, 0)
            elif self.comboid == 2:
                self.setGeometry(rect.left, rect.bottom - 80 , 50 + 1.5*self.layersize, 50 + 1*self.layersize)
                button_open.move(0, 0)
            elif self.comboid == 3:
                self.setGeometry(rect.right - 90, rect.top , 50 + 1.5*self.layersize, 50 + 1*self.layersize)
                button_open.move(75, 0)
            elif self.comboid == 4:
                self.setGeometry(rect.right - 90, rect.bottom/2 , 50 + 1.5*self.layersize, 50 + 1*self.layersize)
                button_open.move(75, 0)
            elif self.comboid == 5:
                self.setGeometry(rect.right - 90, rect.bottom - 80, 50 + 1.5*self.layersize, 50 + 1*self.layersize)
                button_open.move(75, 0)
                    # strech入れる場所
            self.strechBox = QtWidgets.QHBoxLayout()
            self.strechBox.setContentsMargins(0, 0, 0, 0)
            self.strechBox.addStretch(2)
            self.openBox.insertLayout(1, self.strechBox, 1)
            self.onetimeFlag = 1

            self.flag = 1

    def setcurrenttime(self):
        currentTime = QtCore.QDateTime.currentDateTime().toString('hh:mm')
        self.timedisplay.display(currentTime)

    def addtask(self):
        #タスク
        self.task =  QtWidgets.QGroupBox(self.scrollAreaWidget)
        self.scrollAreaWidgetLayout.addWidget(self.task)
        #詳細
        self.detailBox = QtWidgets.QHBoxLayout(self.task)
        #チェックボックス
        checkBox1 = QtWidgets.QCheckBox("First", self.task)
        self.detailBox.insertWidget(-1, checkBox1)
        taskLabel = QtWidgets.QLabel("【タスク】", self.task)
        taskLabel.setStyleSheet("color: rgba(0, 0, 0, 255);font-family: impact;font-size:18px;")
        self.detailBox.insertWidget(-1, taskLabel)
        timerLabel = QtWidgets.QLabel("15分", self.task)
        timerLabel.setStyleSheet("color: rgba(0, 0, 0, 255);font-family: impact;font-size:18px;")
        self.detailBox.insertWidget(-1, timerLabel)
        quantityLabel = QtWidgets.QLabel("3回", self.task)
        quantityLabel.setStyleSheet("color: rgba(0, 0, 0, 255);font-family: impact;font-size:18px;")
        self.detailBox.insertWidget(-1, quantityLabel)
        

    @staticmethod
    #ウィンドウハンドルを返す
    def __get_handle(process_name):        
        return user32.FindWindowW(0, process_name)
    
    # 背景が描画されなくなるので、paintEvent側で描画する。
    def paintEvent(self,Event):
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