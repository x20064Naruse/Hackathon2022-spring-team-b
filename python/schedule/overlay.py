
#!python3
# encoding:utf-8
import ctypes
import ctypes.wintypes
from queue import Empty
from traceback import print_last
import datetime
import getTaskList
import profileManeger

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
        self.remainsec = 0
        self.remainseca = 0
        self.remainmin = 0
        self.remainmina = 0
        self.remainhour = 0
        self.tasknum = 0 #表示されてるタスクの数
        self.titlename = "" #選択されているタイトル

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
        # propertiesボタン
        global button_pro
        button_pro =  QtWidgets.QPushButton("properties", self)
        button_pro.clicked.connect(self.makeWindow)
        button_pro.setStyleSheet("background-color: rgba(170, 170, 170, 225);")
        button_pro.move(20, 0)
        button_pro.resize(0, 15)
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
        timer = QtCore.QTimer(self)
        # timer.timeout.connect(self.setremaintime)
        self.label = QtWidgets.QLabel("")
        # self.setremaintime()
        timer.start(10)
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
        self.centralwidgetLayout.addLayout(self.scrollBox, 4)
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
            button_pro.resize(120, 15)
            print("open")
            self.flag = 0
            self.setGeometry(rect.left, rect.top, (rect.right - rect.left)/3, rect.bottom - rect.top)
            self.setStyleSheet("background-color: rgba(170, 170, 170, 225);")
            #時計
            self.clockBox.setContentsMargins(0, 0, 0, 0)
            # 設定
            self.optionArea = QtWidgets.QHBoxLayout()
            self.scrollBox.insertLayout(0, self.optionArea, 1)
            self.scrollBox.setContentsMargins(0, 0, 0, 0)
            #ゲームタイトル
            self.titleBox = QtWidgets.QComboBox(self)
            self.titleBox.addItems(['Apex', 'Minecraft', 'Masterduel'])
            self.optionArea.insertWidget(0, self.titleBox)
            # scroll
            self.scrollArea = QtWidgets.QScrollArea(self)
            self.scrollArea.setWidgetResizable(True)
            self.scrollAreaWidget = QtWidgets.QWidget()
            self.scrollAreaWidgetLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidget)
            self.scrollArea.setWidget(self.scrollAreaWidget)
            self.scrollBox.insertWidget(1, self.scrollArea, 10)
            self.titleBox.setCurrentText(self.titlename)
            self.tasklist, self.tmp0 = getTaskList.getTaskList(self.titlename)
            for tasks in self.tasklist:
                print(tasks)
                gametitle = tasks.game_title
                taskname = tasks.task_name
                required = tasks.required_time
                priority = tasks.priority
                quantity = tasks.quantity
                self.addtask(gametitle, taskname, required, priority, quantity)
            self.titleBox.currentIndexChanged.connect(self.updatetask)

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
            print(self.remainsec)
            button_pro.resize(0, 0)
            self.comboid = self.comboBox.currentIndex()
            self.scrollArea.deleteLater()
            self.sliderBox.deleteLater()
            self.slider.deleteLater()
            self.spinbox.deleteLater()
            self.comboBox.deleteLater()
            self.titleBox.deleteLater()

            self.setStyleSheet("background-color: rgba(170, 170, 170, 0);")
            # if self.remainmin >= 60:
            #     self.remainhour = self.remainmin // 60
            #     self.remainmina = self.remainmin % 60
            # if self.remainhour == 0:
            #     self.label.setText(str(self.remainmin) + "m")
            # else:
            #     self.label.setText(str(self.remainhour) + "h" + str(self.remainmina) + "m")

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

    def setremaintime(self):
        self.temp1, self.remaintime = getTaskList.getTaskList('Apex')
        self.label.setText(str(self.remaintime))

    def addtask(self, gametitle, taskname, requiredtime, priority, quantity):
        #タスク
        self.task =  QtWidgets.QGroupBox(self.scrollAreaWidget)
        self.scrollAreaWidgetLayout.addWidget(self.task)
        #詳細
        self.detailBox = QtWidgets.QHBoxLayout(self.task)
        #チェックボックス
        checkBox1 = QtWidgets.QCheckBox("", self.task)
        self.detailBox.insertWidget(-1, checkBox1)
        taskLabel = QtWidgets.QLabel("【" + taskname + "】", self.task)
        taskLabel.setStyleSheet("color: rgba(0, 0, 0, 255);font-family: impact;font-size:18px;")
        self.detailBox.insertWidget(-1, taskLabel)
        timerLabel = QtWidgets.QLabel(str(requiredtime) + "分", self.task)
        timerLabel.setStyleSheet("color: rgba(0, 0, 0, 255);font-family: impact;font-size:18px;")
        self.detailBox.insertWidget(-1, timerLabel)
        quantityLabel = QtWidgets.QLabel(str(quantity) + "回", self.task)
        quantityLabel.setStyleSheet("color: rgba(0, 0, 0, 255);font-family: impact;font-size:18px;")
        self.detailBox.insertWidget(-1, quantityLabel)

    def updatetask(self):
        for a in self.tasklist:
            self.detailBox.deleteLater()
        
        self.tasklist, self.tmp0 = getTaskList.getTaskList("Apex")
        for tasks in self.tasklist:
            gametitle = tasks.game_title
            taskname = tasks.task_name
            required = tasks.required_time
            priority = tasks.priority
            quantity = tasks.quantity
            self.addtask(gametitle, taskname, required, priority, quantity)
    
    # def makeWindow(self):
    #     subWindow = SubWindow(self)
    #     subWindow.show()
        
    # # サブウィンドウから実行
    # def setParam(self, param):
    #     self.label.setText(param)

    @staticmethod
    #ウィンドウハンドルを返す
    def __get_handle(process_name):        
        return user32.FindWindowW(0, process_name)
    
    # 背景が描画されなくなるので、paintEvent側で描画する。
    def paintEvent(self,Event):
        painter = QtGui.QPainter(self)
        painter.fillRect(0, 0, self.width(), self.height(), painter.background())

class SubWindow:
    def __init__(self, parent=None):
        self.w = QtWidgets.QDialog(parent)
        self.parent = parent
        titlename = "" #選択されているタイトル
        #ゲームタイトル
        self.titleBox = QtWidgets.QComboBox(self)
        self.titleBox.addItems(['Apex', 'Minecraft', 'Masterduel'])
        self.optionArea.insertWidget(0, self.titleBox)
        self.scrollBox = QtWidgets.QVBoxLayout()
        self.scrollBox.setContentsMargins(0, 0, 0, 0)
        # scroll
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidget = QtWidgets.QWidget()
        self.scrollAreaWidgetLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidget)
        self.scrollArea.setWidget(self.scrollAreaWidget)
        self.scrollBox.addWidget(1, self.scrollArea, 10)
        self.titleBox.setCurrentText(titlename)
        self.tasklist, self.tmp0 = getTaskList.getTaskList(titlename)
        for tasks in self.tasklist:
            print(tasks)
            gametitle = tasks.game_title
            taskname = tasks.task_name
            required = tasks.required_time
            priority = tasks.priority
            quantity = tasks.quantity
            self.edittask(gametitle, taskname, required, priority, quantity)
        self.titleBox.currentIndexChanged.connect(self.updatetask)

        button = QtWidgets.QPushButton('送信')
        button.clicked.connect(self.setParamOriginal)

        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(button)

        self.w.setLayout(layout)

    def edittask(self, gametitle, taskname, requiredtime, priority, quantity):
        #タスク
        self.task =  QtWidgets.QGroupBox(self.scrollAreaWidget)
        self.scrollAreaWidgetLayout.addWidget(self.task)
        #詳細
        self.detailBox = QtWidgets.QHBoxLayout(self.task)
        taskLabel = QtWidgets.QLabel("【" + taskname + "】", self.task)
        taskLabel.setStyleSheet("color: rgba(0, 0, 0, 255);font-family: impact;font-size:18px;")
        self.detailBox.insertWidget(-1, taskLabel)
        timerLabel = QtWidgets.QLabel(str(requiredtime) + "分", self.task)
        timerLabel.setStyleSheet("color: rgba(0, 0, 0, 255);font-family: impact;font-size:18px;")
        self.detailBox.insertWidget(-1, timerLabel)
        quantityLabel = QtWidgets.QLabel(str(quantity) + "回", self.task)
        quantityLabel.setStyleSheet("color: rgba(0, 0, 0, 255);font-family: impact;font-size:18px;")
        self.detailBox.insertWidget(-1, quantityLabel)

    # ここで親ウィンドウに値を渡している
    def setParamOriginal(self):
        self.parent.setParam(self.edit.text())

    def show(self):
        self.w.exec_()

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