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

    def set_config(self, data):
        self.config_category = data.get('category', [])
        self.config_ignore = data.get('ignore', [])

    def keep_saving_config(self, timeout=1000):
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
        # print(data)
        for name, value in vars(self).items():
            key = name
            type_name = type(getattr(self, name))
            # parent_name = self.get_parent_name(value)
            if name in self.config_ignore:
                print('name:%s'% name)
                continue
            if type_name in self.config_ignore:
                print('type_name:%s'% type_name)
                continue
            # if parent_name in self.config_ignore:
            #     print('parent_name:%s'% parent_name)
            #     continue
            def get_value(key, data_dict):
                '''get value in dict'''
                if isinstance(data_dict, dict):
                    for x in data_dict:
                        if x == key:
                            return data_dict[x]
                        elif isinstance(data_dict[x], dict):
                            tmp = get_value(key, data_dict[x])
                            if tmp:return tmp
                            else: continue
            if type_name == QtWidgets.QDoubleSpinBox:
                conf = get_value(key, data)
                value.setValue(conf)
            if type_name == QtWidgets.QLineEdit:
                conf = get_value(key, data)
                value.setText(conf)
            if type_name == QtWidgets.QTextEdit:
                conf = get_value(key, data)
                value.setText(conf)
            if type_name == QtWidgets.QCheckBox:
                conf = get_value(key, data)
                value.setChecked(conf)
            if type_name == QtWidgets.QTimeEdit:
                conf = get_value(key, data)
                mytime = time.strftime('%H:%M:%S', conf)
                value.setTime(QtCore.QTime.fromString(mytime, "hh:mm:ss"))
            if type_name == QtWidgets.QDateEdit:
                conf = get_value(key, data)
                value.setDateTime(conf)
            if type_name == QtWidgets.QDateTimeEdit:
                conf = get_value(key, data)
                value.setDateTime(conf)
            if type_name == QtWidgets.QRadioButton:
                conf = get_value(key, data)
                value.setChecked(conf)
            if type_name == QtWidgets.QComboBox:
                conf = get_value(key, data)
                value.setCurrentIndex(conf)
            if type_name == QtWidgets.QSpinBox:
                conf = get_value(key, data)
                data.setdefault(key, value.setValue(conf))
            if type_name == QtWidgets.QDoubleSpinBox:
                conf = get_value(key, data)
                data.setdefault(key, value.setValue(conf))

    def get_parent_name(self, obj):
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
        data = {}
        for name, value in vars(self).items():
            key = name
            type_name = type(getattr(self, name))
            if type_name == QtWidgets.QDoubleSpinBox:
                data[key] = value.value()
            if type_name == QtWidgets.QLineEdit:
                data[key] = value.text()
            if type_name == QtWidgets.QTextEdit:
                data.setdefault(key,value.toPlainText())
            if type_name == QtWidgets.QCheckBox:
                data[key] = value.isChecked()
            if type_name == QtWidgets.QTimeEdit:
                time_str = value.time().toString("hh:mm:ss")
                data[key] = time.strptime(time_str,'%H:%M:%S')
            if type_name == QtWidgets.QDateEdit:
                date_str = value.date().toString("yyyy/MM/dd")
                data[key] = datetime.datetime.strptime(date_str,'%Y/%m/%d')
            if type_name == QtWidgets.QDateTimeEdit:
                dt_str = value.dateTime().toString("yyyy/MM/dd hh:mm:ss")
                data[key] = datetime.datetime.strptime(dt_str,'%Y/%m/%d %H:%M:%S')
            if type_name == QtWidgets.QRadioButton:
                data[key] = value.isChecked()
            if type_name == QtWidgets.QComboBox:
                data[key] = value.currentIndex()
            if type_name == QtWidgets.QSpinBox:
                data[key] = value.value()
            if type_name == QtWidgets.QDoubleSpinBox:
                data[key] = value.value()
        def tree_dict(data):
            widgets = list(tuple(data))
            for widget in widgets:
                tmp_obj = getattr(self, widget)
                parent_name = self.get_parent_name(tmp_obj)
                if parent_name in self.config_category:
                    if parent_name in data:
                        data[parent_name][widget] = data.pop(widget)
                    else:
                        data[parent_name] = {widget:data.pop(widget)}
            return data
        return tree_dict(data)
    
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
            self.set_config({'category':['myframe','Layout','gridLayout'],
                             'ignore':['lineEdit', QtWidgets.QTextEdit]})
            self.keep_saving_config(1000)
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    ex.show()
    print('self.config:%s' % ex.config)
    sys.exit(app.exec_())

