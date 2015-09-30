# QuickStart

1. Put ui_config.py in your program dir and import the class.
2. Import the class UiConfig and inherited in your class.
3. Add line 'self.set_config(your_config_dict)' after self.setupUi() if needed.
4. Add line 'self.keep_saving_config()' after self.setupUi().

That's all

Example:

    from Ui_ui_config import Ui_Dialog
    class Example(QtWidgets.QWidget, Ui_Dialog, UiConfig):
        def __init__(self):
            super(Example, self).__init__()
            self.setupUi(self)
            self.set_config({'category':['myframe',
                                         'frame3','groupBox_in_frame3','frame_in_frame3',
                                         'groupBox_2','vLayout','frame_in_groupbox2',
                                         'gridLayout',# this works,see notice
                                         'hLayout' # this doesn't work, the same as vLayout
                                         ],
                             'ignore':['lineEdit','groupBox', QtWidgets.QTextEdit]})
            self.keep_saving_config(1000)
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    ex.show()
    import pprint
    pprint.pprint('self.config:%s' % ex.config)
    sys.exit(app.exec_())

# Settings

- Items in category can be collected in a dict,it should be a name of a container widget or layout.
- Items in ignore can't be loaded to interface when program start.
- We can add varname,QObject_style,category_name in ignore dict.

As the example
 
Start the program and set some value:

![settings][1]

then restart the program.We got a dict:

    self.config:{'gridLayout':{'lineEdit_in_hLayout':'dfas23f','lineEdit_in_gridLayout':'sfdwer'},
                 'frame3':{'groupBox_in_frame3':{'doubleSpinBox_4':2.0},
                           'frame_in_frame3':{'lineEdit_7':'sd2'}},
                 'lineEdit_6':'wesd',
                 'checkBox_2':True,
                 'dateTimeEdit':datetime.datetime(2002, 1, 1, 0, 0),
                 'dateEdit':datetime.datetime(1997, 1, 1, 0, 0),
                 'checkBox':True,
                 'doubleSpinBox_3_in_myframe2':2.0,
                 'comboBox':1,
                 'timeEdit':time.struct_time(tm_year=1900, tm_mon=1, tm_mday=1, tm_hour=2, tm_min=0, tm_sec=0, tm_wday=0, tm_yday=1, ' tm_isdst=-1),
                 'radioButton_2':True,
                 'groupBox_2':{'spinBox_5_in_groupbox':4,
                               'spinBox_2_in_groupbox':1,
                               'spinBox_4_in_groupbox':2,
                               'spinBox_3_in_groupbox':3,
                               'frame_in_groupbox2':{'lineEdit_4':'sdf1',
                                                     'lineEdit_9':'sdf12',
                                                     'lineEdit_3':'sdf13',
                                                     'lineEdit_8':'3dsf'}},
                 'myframe':{'spinBox_in_myframe':2,
                            'lineEdit_in_myframe':'s23',
                            'doubleSpinBox_in_myframe':2.0,
                            'lineEdit_2_in_myframe':'sdf23'}}

Parameter in  function self.keep_saving_config(1000) control the frequency of updates on self.config.

# Notice

If the type of category is Layout(Vertical,Horizontal,Grid,Form),only the outermost one can work.In the example,only gridLayout works.

[1]: /201509301.jpg
