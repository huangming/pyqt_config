#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Created Time: 2015/8/25 17:46:50
#author: Cactus
import os
import sys
from PyQt5 import QtCore, QtWidgets
import pickle
import time
import datetime

class UiConfig(QtCore.QObject):

    def config_init(self):
        def set_timeEdit(value, conf):
            mytime = time.strftime('%H:%M:%S', conf)
            value.setTime(QtCore.QTime.fromString(mytime, "hh:mm:ss"))
        def get_timeEdit(value):
            time_str = value.time().toString("hh:mm:ss")
            return time.strptime(time_str,'%H:%M:%S')
        def get_dateEdit(value):
            date_str = value.date().toString("yyyy/MM/dd")
            return datetime.datetime.strptime(date_str,'%Y/%m/%d')
        def get_datetimeEdit(value):
            dt_str = value.dateTime().toString("yyyy/MM/dd hh:mm:ss")
            return datetime.datetime.strptime(dt_str,'%Y/%m/%d %H:%M:%S')
        self.config_function = {QtWidgets.QDoubleSpinBox:(QtWidgets.QDoubleSpinBox.value,0,
                            QtWidgets.QDoubleSpinBox.setValue),
                        QtWidgets.QSpinBox:(QtWidgets.QSpinBox.value,0,
                            QtWidgets.QSpinBox.setValue),
                        QtWidgets.QLineEdit:(QtWidgets.QLineEdit.text,'',
                            QtWidgets.QLineEdit.setText),
                        QtWidgets.QTextEdit:(QtWidgets.QTextEdit.toPlainText,'',
                            QtWidgets.QTextEdit.setText),
                        QtWidgets.QCheckBox:(QtWidgets.QCheckBox.isChecked,False,
                            QtWidgets.QCheckBox.setChecked),
                        QtWidgets.QRadioButton:(QtWidgets.QRadioButton.isChecked,False,
                            QtWidgets.QRadioButton.setChecked),
                        QtWidgets.QComboBox:(QtWidgets.QComboBox.currentIndex,0,
                            QtWidgets.QComboBox.setCurrentIndex),
                        QtWidgets.QTimeEdit:(get_timeEdit,time.time(),
                            set_timeEdit),
                        QtWidgets.QDateEdit:(get_dateEdit,datetime.datetime.today(),
                            QtWidgets.QDateEdit.setDateTime),
                        QtWidgets.QDateTimeEdit:(get_datetimeEdit,datetime.datetime.today(),
                            QtWidgets.QDateTimeEdit.setDateTime)
                        }
 
    def set_config(self, data):
        self.config_category = data.get('category', [])
        self.config_ignore = data.get('ignore', [])

    def keep_saving_config(self, timeout=1000):
        self.config_init()
        try:
            self.config = self.read_config()
            # print(self.config)
            self.load_config(self.config)
        except:
            pass
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.save_config)
        timer.start(timeout)

    def load_config(self, mydata):
        if not mydata:
            return False
        data = mydata
        all_item = [(x[0], x[1]) for x in vars(self).items() if isinstance(x[1],QtCore.QObject)]
        for name, value in all_item:
            key = name
            type_name = type(getattr(self, name))
            parent_name = value.parent().objectName()
            if name in self.config_ignore:
                continue
            if type_name in self.config_ignore:
                continue
            if parent_name in self.config_ignore:
                continue
            def get_value_in_dict(key, data_dict):
                '''get value in dict'''
                if isinstance(data_dict, dict):
                    for x in data_dict:
                        if x == key:
                            return data_dict[x]
                        elif isinstance(data_dict[x], dict):
                            tmp = get_value_in_dict(key, data_dict[x])
                            if tmp:return tmp
                            else: continue
            conf = get_value_in_dict(key, data)
            def set_value(Qobject, value):
                type_name = type(Qobject)
                if type_name in self.config_function:
                    if not value:value = self.config_function[type_name][1]
                    data_value = self.config_function[type_name][2](Qobject, value)
            set_value(value, conf)

    def get_parent_name(self, obj):
        if not isinstance(obj, QtCore.QObject):
            return 'Not QObject'
        layout_list = [QtWidgets.QVBoxLayout,
                QtWidgets.QHBoxLayout,QtWidgets.QGridLayout,QtWidgets.QFormLayout]
        parent = obj.parent()
        if type(parent) == QtWidgets.QWidget:
            children = parent.children()
            for child in children:
                if type(child) in layout_list:
                    return child.objectName()
        return parent.objectName()

    def get_config(self):
        def get_value(Qobject):
            type_name = type(Qobject)
            if not type_name in self.config_function:
                return None
            else:
                data_value = self.config_function[type_name][0](Qobject)
                return data_value if data_value else self.config_function[type_name][1]
        def tree_dict(data):
            widgets = list(tuple(data))
            layout_list = [QtWidgets.QVBoxLayout,
                    QtWidgets.QHBoxLayout,QtWidgets.QGridLayout,QtWidgets.QFormLayout]
            for widget in widgets:
                tmp_obj = getattr(self, widget)
                if type(tmp_obj) in layout_list:
                    continue
                parent_name = self.get_parent_name(tmp_obj)
                if parent_name in self.config_category:
                    if parent_name in data:
                        data[parent_name][widget] = data.pop(widget)
                    else:
                        data[parent_name] = {widget:data.pop(widget)}
            return data
        data = {}
        all_item = [(x[0], x[1]) for x in vars(self).items() if isinstance(x[1],QtCore.QObject)]
        for name, value in all_item:
            data_value = get_value(value)
            if data_value: data[name] = data_value
        for i in range(len(all_item)):
            data = tree_dict(data)
        return data
    
    def save_config(self, data = None, path = None):
        if path == None:
            path = getattr(sys.modules['__main__'], '__file__', 'data.pkl')
            path = os.path.basename(path.replace('.py', '.pkl'))
        if not data:
            self.config = self.get_config()
            data = self.config
        output = open(path, 'wb')
        pickle.dump(data, output)
        output.close()

    def read_config(self, path = None):
        data = {}
        if path == None:
            path = getattr(sys.modules['__main__'], '__file__', 'data.pkl')
            path = os.path.basename(path.replace('.py', '.pkl'))
        try:
            input_file = open(path, 'rb')
            data = pickle.load(input_file)
            input_file.close()
        except:
            pass
        return data

if __name__ == '__main__':
    from Ui_ui_config import Ui_Dialog
    class Example(QtWidgets.QWidget, Ui_Dialog, UiConfig):
        def __init__(self):
            super(Example, self).__init__()
            self.setupUi(self)
            self.set_config({'category':['myframe',
                                         'frame3','groupBox_in_frame3','frame_in_frame3',
                                         'groupBox_2','vLayout','frame_in_groupbox2',
                                         'gridLayout',# this works,see readme.
                                         'hLayout' # this doesn't work, the same as vLayout
                                         ],
                             'ignore':['lineEdit','groupBox', QtWidgets.QTextEdit]})
            self.keep_saving_config(1000)
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    ex.show()
    import pprint
    pprint.pprint('self.config:%s' % ex.config)
    print(ex.groupBox_in_frame3.parent().objectName())
    sys.exit(app.exec_())

