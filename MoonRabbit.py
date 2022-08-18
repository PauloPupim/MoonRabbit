import re
import sys
import json

from datetime import timedelta

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QDoubleSpinBox, QAbstractSpinBox, QFileDialog, QMessageBox, QSpinBox, QLineEdit, QWidget
)
from PyQt6 import QtCore
from PyQt6.QtCore import QEvent, QObject


# Command for generate ui class/file
# pyuic6.exe -o ui_MoonRabbitWindow.py .\ui_files\MoonRabbitWindow_.ui
from ui_MoonRabbitWindow import Ui_MainWindow
from ui_CalculateTimeWindow import Ui_CalculateTime

# Command to create rc_img
# pyside6-rcc.exe .\img\img_files.qrc -o rc_img.py
import rc_img

# Class to install a filter in doublespinbox avoiding them getting focus by hover
class MouseWheelWidgetAdjustmentGuard(QObject):
    def __init__(self, parent: QObject):
        super().__init__(parent)

    def eventFilter(self, o: QObject, e: QEvent) -> bool:
        widget: QWidget = o
        if e.type() == QEvent.Type.Wheel and not widget.hasFocus():
            e.ignore()
            return True
        return super().eventFilter(o, e)


class CalculateTime(QWidget, Ui_CalculateTime):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignals()

    def connectSignals(self):
        self.cb_rate_time.currentTextChanged.connect(self.updateTime)
        self.dsb_rate.valueChanged.connect(self.updateTime)
        self.dsb_needed.valueChanged.connect(self.updateTime)

    def updateTime(object, value):
        rate = object.dsb_rate.value()
        needed = object.dsb_needed.value()
        time_rate = object.cb_rate_time.currentText()
        match time_rate:
            case 'Hours':
                time = 1/60
            case 'Minutes':
                time = 1
            case 'Seconds':
                time = 60
        if rate <= 0:
            result = ''
        else:
            minutes = needed / rate / time
            result = '' if rate <= 0 else str(timedelta(minutes=minutes)).replace(',', '')
            result = re.sub('\..*', '', result)

        object.lineedit_result.setText(result)


class MoonRabbitWindow(QMainWindow, Ui_MainWindow):
    # Level = Enum('LEVEL', 'U1 U2 U3 U4 E1 E2 E3 E4 L1 L2 L3 L4 S1 S2 S3 S4')

    # U1 = 1
    # U2 = 2
    # U3 = 3
    # U4 = 4
    # E1 = 5
    # E2 = 6
    # E3 = 7
    # E4 = 8
    # L1 = 9
    # L2 = 10
    # L3 = 11
    # L4 = 12
    # S1 = 13
    # S2 = 14
    # S3 = 15
    # S4 = 16
    current_save_file = None
    unsaved_flag = False
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()

    def closeEvent(self, event):
        if self.unsaved_flag is True:
            result = QMessageBox.question(self,
                                       "Confirm exit...",
                                       "There is unsaved file. Do you want to save?",
                                       QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard)

            if result == QMessageBox.StandardButton.Save:
                self.save_file()
            event.accept()
        else:
            event.accept()

    def preventAnnoyingSpinboxScrollBehaviour(self, control: QAbstractSpinBox) -> None:
        control.setFocusPolicy(QtCore.FocusPolicy.StrongFocus)
        control.installEventFilter(self.MouseWheelWidgetAdjustmentGuard(control))

    def set_unsaved_flag(self):
        self.unsaved_flag = True
        self.setWindowTitle('Moon Rabbit Calculator**')

    def set_saved_flag(self):
        self.unsaved_flag = False
        self.setWindowTitle('Moon Rabbit Calculator')

    def connectSignalsSlots(self):
        self.actionSave_File.triggered.connect(self.save_file)
        self.actionLoad_File.triggered.connect(self.load_file)
        self.actionCalculate_Time.triggered.connect(self.show_calculate_window)

        for spinbox in self.findChildren(QDoubleSpinBox):
            name = spinbox.objectName()
            character = 'nia' if name[-2:] == '_2' else 'rab'
            type = name[6:] if character == 'rab' else name[6:-2]
            spinbox.valueChanged.connect(self.calculaNeeded)
            spinbox.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
            spinbox.installEventFilter(MouseWheelWidgetAdjustmentGuard(spinbox))
            spinbox.valueChanged.connect(self.set_unsaved_flag)

            if type == 'needed':
                spinbox.valueChanged.connect(self.calculaTime)

        for spinbox in self.findChildren(QSpinBox):
            spinbox.valueChanged.connect(self.calculaTime)
            spinbox.valueChanged.connect(self.set_unsaved_flag)

    def show_calculate_window(self):
        # But if you see it it will only be visible for a fraction of a second. What's happening?
        # Inside this method, we are creating our window (widget) object, storing it in the variable w and showing it.
        # However, once we leave the method we no longer have a reference to the w variable (it is a local variable) and
        # so it will be cleaned up – and the window destroyed. To fix this we need to keep a reference to the window somewhere, for example on the self object.
        self.calculate = CalculateTime()
        self.calculate.show()

    def calculaTime(object, value):
        name = object.sender().objectName()
        level = name[3:5]
        character = 'nia' if name[-2:] == '_2' else 'rab'
        type = name[6:] if character == 'rab' else name[6:-2]

        if type == 'needed':
            needed = value
            rate = object.findChild(QSpinBox, 'sb_' + level + '_rate').value()
        else:
            needed = object.findChild(QDoubleSpinBox, 'sb_' + level + '_needed').value()
            rate = value

        mnt = '' if rate <= 0 else str(timedelta(minutes=needed/(rate/60))).replace(',', '')

        mnt = re.sub('\..*' ,'',mnt)

        object.findChild(QLineEdit, 'le_' + level + '_time').setText(mnt)

    def calculaNeeded(object, value):
        name = object.sender().objectName()
        character = 'nia' if name[-2:] == '_2' else 'rab'
        level = name[3:5]
        type = name[6:] if character == 'rab' else name[6:-2]

        if (character == 'rab'):
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
                        object.sb_l4_needed.setValue(3*(object.sb_s1_needed.value() if object.sb_s1_needed.value()>0 else object.sb_s1_wanted.value()) - value)
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
        else:
            if type == 'wanted' or type == 'needed':
                match level:
                    case 's4':
                        object.sb_s3_needed_2.setValue(value * 3 - object.sb_s3_atual_2.value())
                    case 's3':
                        object.sb_s2_needed_2.setValue(value * 3 - object.sb_s2_atual_2.value())
                    case 's2':
                        object.sb_s1_needed_2.setValue(value * 3 - object.sb_s1_atual_2.value())
                    case 's1':
                        object.sb_l4_needed_2.setValue(value * 3 - object.sb_l4_atual_2.value())
                    case 'l4':
                        object.sb_l3_needed_2.setValue(value * 5 - object.sb_l3_atual_2.value())
                    case 'l3':
                        object.sb_l2_needed_2.setValue(value * 5 - object.sb_l2_atual_2.value())
                    case 'l2':
                        object.sb_l1_needed_2.setValue(value * 5 - object.sb_l1_atual_2.value())
                    case 'l1':
                        object.sb_e4_needed_2.setValue(value * 5 - object.sb_e4_atual_2.value())
                    case 'e4':
                        object.sb_e3_needed_2.setValue(value * 5 - object.sb_e3_atual_2.value())
                    case 'e3':
                        object.sb_e2_needed_2.setValue(value * 5 - object.sb_e2_atual_2.value())
                    case 'e2':
                        object.sb_e1_needed_2.setValue(value * 5 - object.sb_e1_atual_2.value())
                    case 'e1':
                        object.sb_u4_needed_2.setValue(value * 5 - object.sb_u4_atual_2.value())
                    case 'u4':
                        object.sb_u3_needed_2.setValue(value * 5 - object.sb_u3_atual_2.value())
                    case 'u3':
                        object.sb_u2_needed_2.setValue(value * 5 - object.sb_u2_atual_2.value())
                    case 'u2':
                        object.sb_u1_needed_2.setValue(value * 5 - object.sb_u1_atual_2.value())

            if type == 'atual':
                match level:
                    case 's4':
                        object.sb_s4_needed_2.setValue((
                                                         object.sb_s4_needed_2.value() if object.sb_s4_needed_2.value() > 0 else object.sb_s4_wanted_2.value()) - value)
                    case 's3':
                        object.sb_s3_needed_2.setValue(3 * (
                            object.sb_s4_needed_2.value() if object.sb_s4_needed_2.value() > 0 else object.sb_s4_wanted_2.value()) - value)
                    case 's2':
                        object.sb_s2_needed_2.setValue(3 * (
                            object.sb_s3_needed_2.value() if object.sb_s3_needed_2.value() > 0 else object.sb_s3_wanted_2.value()) - value)
                    case 's1':
                        object.sb_s1_needed_2.setValue(3 * (
                            object.sb_s2_needed_2.value() if object.sb_s2_needed_2.value() > 0 else object.sb_s2_wanted_2.value()) - value)
                    case 'l4':
                        object.sb_l4_needed_2.setValue(3 * (
                            object.sb_s1_needed_2.value() if object.sb_s1_needed_2.value() > 0 else object.sb_s1_wanted_2.value()) - value)
                    case 'l3':
                        object.sb_l3_needed_2.setValue(5 * (
                            object.sb_l4_needed_2.value() if object.sb_l4_needed_2.value() > 0 else object.sb_l4_wanted_2.value()) - value)
                    case 'l2':
                        object.sb_l2_needed_2.setValue(5 * (
                            object.sb_l3_needed_2.value() if object.sb_l3_needed_2.value() > 0 else object.sb_l3_wanted_2.value()) - value)
                    case 'l1':
                        object.sb_l1_needed_2.setValue(5 * (
                            object.sb_l2_needed_2.value() if object.sb_l2_needed_2.value() > 0 else object.sb_l2_wanted_2.value()) - value)
                    case 'e4':
                        object.sb_e4_needed_2.setValue(5 * (
                            object.sb_l1_needed_2.value() if object.sb_l1_needed_2.value() > 0 else object.sb_l1_wanted_2.value()) - value)
                    case 'e3':
                        object.sb_e3_needed_2.setValue(5 * (
                            object.sb_e4_needed_2.value() if object.sb_e4_needed_2.value() > 0 else object.sb_e4_wanted_2.value()) - value)
                    case 'e2':
                        object.sb_e2_needed_2.setValue(5 * (
                            object.sb_e3_needed_2.value() if object.sb_e3_needed_2.value() > 0 else object.sb_e3_wanted_2.value()) - value)
                    case 'e1':
                        object.sb_e1_needed_2.setValue(5 * (
                            object.sb_e2_needed_2.value() if object.sb_e2_needed_2.value() > 0 else object.sb_e2_wanted_2.value()) - value)
                    case 'u4':
                        object.sb_u4_needed_2.setValue(5 * (
                            object.sb_e1_needed_2.value() if object.sb_e1_needed_2.value() > 0 else object.sb_e1_wanted_2.value()) - value)
                    case 'u3':
                        object.sb_u3_needed_2.setValue(5 * (
                            object.sb_u4_needed_2.value() if object.sb_u4_needed_2.value() > 0 else object.sb_u4_wanted_2.value()) - value)
                    case 'u2':
                        object.sb_u2_needed_2.setValue(5 * (
                            object.sb_u3_needed_2.value() if object.sb_u3_needed_2.value() > 0 else object.sb_u3_wanted_2.value()) - value)
                    case 'u1':
                        object.sb_u1_needed_2.setValue(5 * (
                            object.sb_u2_needed_2.value() if object.sb_u2_needed_2.value() > 0 else object.sb_u2_wanted_2.value()) - value)

    def save_file(self):
        if self.current_save_file is None:
            save_file = QFileDialog.getSaveFileName(self, 'Save File', directory='E:\\Documents\\Python_project', filter='*.json')[0]
            if save_file == '':
                return
        else:
            save_file = self.current_save_file

        rab_dict = {}
        nia_dict = {}

        for doublespinbox in self.findChildren(QDoubleSpinBox):
            if doublespinbox.value() != 0:
                # Character Nia has a '_2' suffix in his objects names
                if doublespinbox.objectName()[-2:] == '_2':
                    nia_dict[doublespinbox.objectName()[:-2]] = doublespinbox.value()
                else:
                    rab_dict[doublespinbox.objectName()] = doublespinbox.value()

        for spinbox in self.findChildren(QSpinBox):
            if spinbox.value() != 0:
                # Character Nia has a '_2' suffix in his objects names
                if spinbox.objectName()[-2:] == '_2':
                    nia_dict[spinbox.objectName()[:-2]] = spinbox.value()
                else:
                    rab_dict[spinbox.objectName()] = spinbox.value()

        for lineedit in self.findChildren(QLineEdit):
            if lineedit.objectName()=='qt_spinbox_lineedit':
                continue
            if lineedit.text() != '':
                # Character Nia has a '_2' suffix in his objects names
                if lineedit.objectName()[-2:] == '_2':
                    nia_dict[lineedit.objectName()[:-2]] = lineedit.text()
                else:
                    rab_dict[lineedit.objectName()] = lineedit.text()

        moon_dict = {'rab': rab_dict, 'nia': nia_dict}
        json_file = json.dumps(moon_dict, indent=4, sort_keys=True)

        with open(save_file, 'w') as f:
            f.write(json_file)

        self.current_save_file = save_file
        self.set_saved_flag()

    def load_file(self):
        load_file = QFileDialog.getOpenFileName(self, 'Open File', directory='E:\\Documents\\Python_project\\MoonRabbit\\saves_files', filter='*.json')[0]

        if load_file == '':
            return
        self.blockSignals(True)

        with open(load_file, 'r') as f:
            moon_data = json.loads(f.read())

            for character in moon_data.keys():
                for key in moon_data[character].keys():
                    # Character Nia has a '_2' suffix in his objects names
                    box = key if character == 'rab' else key+'_2'
                    type = key[6:] #if character == 'rab' else key[6:-2]
                    if type == 'atual' or type == 'needed' or type == 'wanted':
                        self.findChild(QDoubleSpinBox, box).setValue(moon_data[character][key])
                    if type == 'rate':
                        self.findChild(QSpinBox, box).setValue(moon_data[character][key])
                    if type == 'time':
                        self.findChild(QLineEdit, box).setText(moon_data[character][key])
        self.current_save_file = load_file
        self.set_saved_flag()
        self.blockSignals(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    moonRabbitWindow = MoonRabbitWindow()
    moonRabbitWindow.show()
    sys.exit(app.exec())
