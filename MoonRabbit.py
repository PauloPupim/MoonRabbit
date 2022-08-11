import sys
import json

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QDoubleSpinBox, QAbstractSpinBox, QFileDialog
)
from PyQt6 import QtCore
from PyQt6.QtCore import QEvent, QObject

# Command for generate ui class/file
# pyuic6.exe -o ui_MoonRabbitWindow.py .\ui_files\MoonRabbitWindow.ui
from ui_MoonRabbitWindow import Ui_MainWindow

# Command to create rc_img
# pyside6-rcc.exe .\img\img_files.qrc -o rc_img.py
import rc_img

# Class to install a filter in spinbox avoinding them getting focus by hover
class MouseWheelWidgetAdjustmentGuard(QObject):
    def __init__(self, parent: QObject):
        super().__init__(parent)

    def eventFilter(self, o: QObject, e: QEvent) -> bool:
        widget: QWidget = o
        if e.type() == QEvent.Type.Wheel and not widget.hasFocus():
            e.ignore()
            return True
        return super().eventFilter(o, e)


class MoonRabbitWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        # self.sb_u1_atual.setValue(1000)

    def connectSignalsSlots(self):
        self.actionSave_File.triggered.connect(self.save_file)
        self.actionLoad_File.triggered.connect(self.loadFile)
        for spinbox in self.findChildren(QDoubleSpinBox):
            spinbox.valueChanged.connect(self.calculaNeeded)
            spinbox.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
            spinbox.installEventFilter(MouseWheelWidgetAdjustmentGuard(spinbox))





    def calculaNeeded(object, value):
        name = object.sender().objectName()
        level = name[3:5]
        type = name[6:]
        # print("name objeto:", name)
        # print("Level objeto:", level)
        # print("Type objeto:", type)
        # print("Value objeto:", value)

        if type == 'wanted' or type == 'needed':
            match level:
                case 's4':
                    object.sb_s3_needed.setValue(value*3 - object.sb_s3_atual.value())
                case 's3':
                    object.sb_s2_needed.setValue(value*3 - object.sb_s2_atual.value())
                case 's2':
                    object.sb_s1_needed.setValue(value*3 - object.sb_s1_atual.value())
                case 's1':
                    object.sb_l4_needed.setValue(value*3 - object.sb_l4_atual.value())
                case 'l4':
                    object.sb_l3_needed.setValue(value*5 - object.sb_l3_atual.value())
                case 'l3':
                    object.sb_l2_needed.setValue(value*5 - object.sb_l2_atual.value())
                case 'l2':
                    object.sb_l1_needed.setValue(value*5 - object.sb_l1_atual.value())
                case 'l1':
                    object.sb_e4_needed.setValue(value*5 - object.sb_e4_atual.value())
                case 'e4':
                    object.sb_e3_needed.setValue(value*5 - object.sb_e3_atual.value())
                case 'e3':
                    object.sb_e2_needed.setValue(value*5 - object.sb_e2_atual.value())
                case 'e2':
                    object.sb_e1_needed.setValue(value*5 - object.sb_e1_atual.value())
                case 'e1':
                    object.sb_u4_needed.setValue(value*5 - object.sb_u4_atual.value())
                case 'u4':
                    object.sb_u3_needed.setValue(value*5 - object.sb_u3_atual.value())
                case 'u3':
                    object.sb_u2_needed.setValue(value*5 - object.sb_u2_atual.value())
                case 'u2':
                    object.sb_u1_needed.setValue(value*5 - object.sb_u1_atual.value())

        if type == 'atual':
            match level:
                case 's4':
                    object.sb_s4_needed.setValue((object.sb_s4_needed.value() if object.sb_s4_needed.value() > 0 else object.sb_s4_wanted.value()) - value)
                case 's3':
                    object.sb_s3_needed.setValue(3*(object.sb_s4_needed.value() if object.sb_s4_needed.value()>0 else object.sb_s4_wanted.value()) - value)
                case 's2':
                    object.sb_s2_needed.setValue(3*(object.sb_s3_needed.value() if object.sb_s3_needed.value()>0 else object.sb_s3_wanted.value()) - value)
                case 's1':
                    object.sb_s1_needed.setValue(3*(object.sb_s2_needed.value() if object.sb_s2_needed.value()>0 else object.sb_s2_wanted.value()) - value)
                case 'l4':
                    object.sb_l4_needed.setValue(5*(object.sb_s1_needed.value() if object.sb_s1_needed.value()>0 else object.sb_s1_wanted.value()) - value)
                case 'l3':
                    object.sb_l3_needed.setValue(5*(object.sb_l4_needed.value() if object.sb_l4_needed.value()>0 else object.sb_l4_wanted.value()) - value)
                case 'l2':
                    object.sb_l2_needed.setValue(5*(object.sb_l3_needed.value() if object.sb_l3_needed.value()>0 else object.sb_l3_wanted.value()) - value)
                case 'l1':
                    object.sb_l1_needed.setValue(5*(object.sb_l2_needed.value() if object.sb_l2_needed.value()>0 else object.sb_l2_wanted.value()) - value)
                case 'e4':
                    object.sb_e4_needed.setValue(5*(object.sb_l1_needed.value() if object.sb_l1_needed.value()>0 else object.sb_l1_wanted.value()) - value)
                case 'e3':
                    object.sb_e3_needed.setValue(5*(object.sb_e4_needed.value() if object.sb_e4_needed.value()>0 else object.sb_e4_wanted.value()) - value)
                case 'e2':
                    object.sb_e2_needed.setValue(5*(object.sb_e3_needed.value() if object.sb_e3_needed.value()>0 else object.sb_e3_wanted.value()) - value)
                case 'e1':
                    object.sb_e1_needed.setValue(5*(object.sb_e2_needed.value() if object.sb_e2_needed.value()>0 else object.sb_e2_wanted.value()) - value)
                case 'u4':
                    object.sb_u4_needed.setValue(5*(object.sb_e1_needed.value() if object.sb_e1_needed.value()>0 else object.sb_e1_wanted.value()) - value)
                case 'u3':
                    object.sb_u3_needed.setValue(5*(object.sb_u4_needed.value() if object.sb_u4_needed.value()>0 else object.sb_u4_wanted.value()) - value)
                case 'u2':
                    object.sb_u2_needed.setValue(5*(object.sb_u3_needed.value() if object.sb_u3_needed.value()>0 else object.sb_u3_wanted.value()) - value)
                case 'u1':
                    object.sb_u1_needed.setValue(5*(object.sb_u2_needed.value() if object.sb_u2_needed.value()>0 else object.sb_u2_wanted.value()) - value)

    def save_file(self):
        save_file = QFileDialog.getSaveFileName(self, 'Save File', filter='*.json')[0]
        if save_file == '':
            return

        moon_dict = {}

        for spinbox in self.findChildren(QDoubleSpinBox):
            moon_dict[spinbox.objectName()] = spinbox.value()

        json_file = json.dumps(moon_dict, indent=4, sort_keys=True)

        with open (save_file, 'w') as f:
            f.write(json_file)

    def loadFile(self):
        load_file = QFileDialog.getOpenFileName(self, 'Open File', filter='*.json')[0]

        if load_file == '':
            return

        with open(load_file, 'r') as f:
            moon_data = json.loads(f.read())
            for key in moon_data.keys():
                self.findChild(QDoubleSpinBox,key).setValue(moon_data[key])




    def preventAnnoyingSpinboxScrollBehaviour(self, control: QAbstractSpinBox) -> None:
        control.setFocusPolicy(Qt.StrongFocus)
        control.installEventFilter(self.MouseWheelWidgetAdjustmentGuard(control))



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Form, Window = uic.loadUiType("ui_files\main.ui")
    #
    # app = QApplication(sys.argv)
    # moonRabbitWin = Window()
    # form = Form()
    # form.setupUi(moonRabbitWin)
    # moonRabbitWin.show()
    #
    # form.sb_u1_atual.setValue(2)

    #moonRabbitWin.sb_u1_atual.setValue(2)
    app = QApplication(sys.argv)
    moonRabbitWindow= MoonRabbitWindow()
    moonRabbitWindow.show()
    sys.exit(app.exec())


