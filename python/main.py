
#!python3
# encoding:utf-8
import ctypes
import ctypes.wintypes

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
        #クリックは下のレイヤへ透過する
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        #タスクバーに表示されない/タイトルバーの削除/常に画面の前面にある
        self.setWindowFlags(QtCore.Qt.Tool|QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint)
        #ウィンドウハンドルをメモ帳に指定
        self.handle = self.__get_handle("ELDEN RING")

        if self.handle:
            #指定時間経過後にSignalを送る
            self.timer = QtCore.QTimer(self)
            #ウィンドウサイズの更新
            self.timer.timeout.connect(self.__windows_resize)
            self.timer.start(10)
        
        #レイアウトの作成
        hbox = QtWidgets.QHBoxLayout()
        vbox = QtWidgets.QVBoxLayout()
        hbox.addLayout(vbox)
        #テキスト
        label = QtWidgets.QLabel("Overlay!!!!")
        label.setStyleSheet("background:transparent; color: rgba(0, 0, 0, 128);font-family: impact;font-size:72px;")
        #中央寄せ
        label.setAlignment(QtCore.Qt.AlignCenter)
        #設置
        vbox.addWidget(label)

        self.setLayout(hbox)

        self.setStyleSheet("background-color: rgba(233, 0, 0, 128);")

        self.showMaximized()

    @staticmethod
    #ウィンドウハンドルを返す
    def __get_handle(process_name):
        return user32.FindWindowW(0, process_name)
    #指定されたウィンドウにリサイズする
    def __windows_resize(self):
        rect = ctypes.wintypes.RECT()
        ctypes.windll.dwmapi.DwmGetWindowAttribute(self.handle, DWMWA_EXTENDED_FRAME_BOUNDS, ctypes.pointer(rect), ctypes.sizeof(rect))
        self.setGeometry(rect.left, rect.top, rect.right - rect.left, rect.bottom - rect.top)
    
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


    exit_code = app.exec_()

    exit(exit_code)