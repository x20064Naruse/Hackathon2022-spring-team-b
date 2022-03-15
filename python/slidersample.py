#これはslider等を使用したサンプルプログラムのコピーです
from PySide import QtCore, QtGui
class IntSlider(QtGui.QWidget):
     
    # シグナルの用意。
    # 変更された値を渡せるように、「QtCore.Signal(int)」として引数があることを通知します。
    valueChanged = QtCore.Signal(int)
     
    def __init__(self, *args, **kwargs):
        super(IntSlider, self).__init__(*args, **kwargs)
         
        layout = QtGui.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
         
        self.__spinBox = QtGui.QSpinBox(self)
        self.__spinBox.setMinimumWidth(80)
        self.__spinBox.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        layout.addWidget(self.__spinBox)
         
        self.__slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        layout.addWidget(self.__slider)
         
        self.__spinBox.valueChanged[int].connect(self.valueChangedCallback)
        self.__slider.valueChanged[int].connect(self.valueChangedCallback)
     
    def valueChangedCallback(self, value):  
        sender = self.sender()
        if sender == self.__spinBox:
            self.__slider.blockSignals(True)
            self.__slider.setValue(value)
            self.__slider.blockSignals(False)
         
        elif sender == self.__slider:
            self.__spinBox.blockSignals(True)
            self.__spinBox.setValue(value)
            self.__spinBox.blockSignals(False)
         
        # シグナルをエミットする。
        # スロットが設定されていなければ何も起きません。
        self.valueChanged.emit(value)
             
    def value(self):
        return self.__spinBox.value()
         
    def setValue(self, value):
        self.__spinBox.setValue(value)
         
    def setRange(self, min, max):
        self.__spinBox.setRange(min, max)
        self.__slider.setRange(min, max)