#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/24 16:24
# @Author  : hedengfeng
# @Site    : 
# @File    : FreqHeatMap.py
# @Software: PyQT5
# @description:
import csv
import math
import os
import random
import sys

from PyQt5.QtGui import QPainter, QColor, QDoubleValidator, QIntValidator
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QGridLayout, QWidget, QLabel, QLineEdit, \
    QFileDialog, QDialog

import cgitb
cgitb.enable()


class MainWidget(QWidget):
    def __init__(self, heat_map):
        super().__init__()
        self.bases_loc_info = ()
        self.heat_map_position = ()
        self.heat_map = None

        self.map_length_label = None
        self.map_height_label = None
        self.heat_map = heat_map

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 200)
        self.setWindowTitle('MainWidget')

        self.mainlayout = QGridLayout()
        self.setLayout(self.mainlayout)
        self.map_length_label = QLabel('仓库长度:')
        self.map_height_label = QLabel('仓库宽度:')

        self.map_length_edit = QLineEdit()
        self.map_length_edit.setText(str(81))
        self.map_length_edit.setAlignment(Qt.AlignRight)
        self.map_length_edit.setMaxLength(6)
        self.map_length_edit.setValidator(QIntValidator(0, 1000, self))

        self.map_height_edit = QLineEdit()
        self.map_height_edit.setText(str(42))
        self.map_height_edit.setAlignment(Qt.AlignRight)
        self.map_height_edit.setMaxLength(4)
        self.map_height_edit.setValidator(QIntValidator(0, 1000, self))

        self.selectFileButton = QPushButton("选择文件")
        self.fileLineEdit = QLineEdit()
        self.selectFileButton.clicked.connect(lambda: self.openFile(self.fileLineEdit.text()))

        self.btn_confirm = QPushButton("confirm", self)
        self.btn_confirm.clicked.connect(self.btnConfirmClicked)

        self.mainlayout.addWidget(self.map_length_label, 0, 0, 1, 1)
        self.mainlayout.addWidget(self.map_length_edit, 0, 1, 1, 1)
        self.mainlayout.addWidget(self.map_height_label, 0, 2, 1, 1)
        self.mainlayout.addWidget(self.map_height_edit, 0, 3, 1, 1)
        self.mainlayout.addWidget(self.selectFileButton, 1, 0, 1, 1)
        self.mainlayout.addWidget(self.fileLineEdit, 1, 1, 1, 3)
        self.mainlayout.addWidget(self.btn_confirm, 2, 3, 1, 1)

        self.show()

    def openFile(self, filePath):
        if os.path.exists(filePath):
            # self, "Open File Dialog", filePath,"Python files(*.py);;Text files(*.txt);;CVS files(*.cvs)"
            path = QFileDialog.getOpenFileName()
        else:
            # "Open File Dialog", "/", "Python files(*.py);;Text files(*.txt);;CVS files(*.cvs)"
            path = QFileDialog.getOpenFileName()

        self.fileLineEdit.setText(str(path[0]))

    def btnConfirmClicked(self):
        #  读取长宽
        length = int(self.map_length_edit.text())
        height = int(self.map_height_edit.text())
        # print(length, height)
        self.heat_map.setProperty(length, height, self.fileLineEdit.text())
        self.heat_map.exec()


class FreqHeatMap(QDialog):
    def __init__(self, length=81, height=42, file_name='E:/linux_share/code/GitHub/PyQT5/test2.csv'):
        # print('FreqHeatMap:', length, height, file_name)
        super().__init__()

        self.painter = None

        self.widget_x = 300
        self.widget_y = 300

        self.space_len = 50

        self.tip_space_len = 20

        self.tip_map_len = 30

        self.color_map = {0: QColor(0, 0, 0), 1: QColor(255, 0, 0), 2: QColor(0, 255, 0), 3: QColor(0, 0, 255),
                          4: QColor(255, 255, 0), 5: QColor(255, 0, 255), 6: QColor(0, 255, 255),
                          7: QColor(0, 125, 125), 8: QColor(125, 0, 125), 9: QColor(255, 255, 255)}

        # self.color_map = {0: QColor(0, 0, 0), 1: QColor(255, 0, 0), 2: QColor(255, 125, 0), 3: QColor(255, 255, 0),
        #                   4: QColor(125, 255, 0), 5: QColor(0, 255, 0), 6: QColor(0, 255, 125),
        #                   7: QColor(0, 255, 255), 8: QColor(0, 125, 255), 9: QColor(0, 0, 255),
        #                   10: QColor(125, 0, 255), 11: QColor(255, 0, 255), 12: QColor(255, 0, 125)}

        self.bases_map_x = self.space_len
        self.bases_map_y = 0
        self.bases_map_length = length * 10
        self.bases_map_height = height * 10

        self.tip_map_x = self.bases_map_length + self.tip_space_len + self.space_len
        self.tip_map_y = 0

        self.bases_file_name = file_name

        self.widget_len = self.bases_map_length + self.space_len*2 + self.tip_space_len + self.tip_map_len
        self.widget_height = self.bases_map_height + self.space_len

        self.bases_loc_info = []
        # self.readBaseLocInfo()
        # print(self.bases_loc_info)

        self.initUI()

    def setProperty(self, length, height, file_name='E:/linux_share/code/GitHub/PyQT5/test2.csv'):
        print('FreqHeatMap setProperty:', length, height, file_name)
        self.bases_map_x = self.space_len
        self.bases_map_y = 0
        self.bases_map_length = length * 10
        self.bases_map_height = height * 10

        self.tip_map_x = self.bases_map_length + self.tip_space_len + self.space_len
        self.tip_map_y = 0

        self.bases_file_name = file_name

        self.widget_len = self.bases_map_length + self.space_len*2 + self.tip_space_len + self.tip_map_len
        self.widget_height = self.bases_map_height + self.space_len

        self.bases_loc_info = []
        self.readBaseLocInfo()
        self.resize(self.widget_len, self.widget_height)

    def initUI(self):
        # print(self.widget_x, self.widget_y, self.widget_len, self.widget_height)
        self.setGeometry(self.widget_x, self.widget_y, self.widget_len, self.widget_height)
        self.setWindowTitle('heatMap')
        # self.show()

    def readBaseLocInfo(self):
        print('readBaseLocInfo', self.bases_file_name)
        csv_file = open(self.bases_file_name, "r")
        reader = csv.reader(csv_file)
        for item in reader:
            # # 忽略第一行
            if reader.line_num == 1:
                continue
            if len(item) >= 2:
                self.bases_loc_info.append(item)
        print(self.bases_loc_info)
        csv_file.close()

    def paintEvent(self, e):
        try:
            print('FreqHeatMap: ', 'self.paintEvent')
            self.painter = QPainter()
            self.painter.begin(self)
            self.drawPoints()
            self.draw_tip_area()

            self.drawXScale()
            self.drawYScale()
            self.painter.end()
        except Exception as e:
            print('Exception:', e)

    def calcCoverBaseCount(self, x, y):
        count = 0
        for tmp in self.bases_loc_info:
            x_len = float(tmp[0]) - x
            y_len = float(tmp[1]) - y
            d = math.sqrt((x_len ** 2) + (y_len ** 2))

            if 13.00 >= d >= 1.00:
                count += 1
        return count

    def draw_tip_area(self):
        group = len(self.color_map)
        step_height = int(self.bases_map_height / group)
        begin_x = self.tip_map_x
        end_x = self.tip_map_len + self.tip_map_x
        for step in range(0, group):
            src_y = self.tip_map_y + (step * step_height)
            dest_y = src_y + step_height
            mid_y = (src_y + dest_y) / 2
            for y in range(src_y, dest_y):
                self.painter.setPen(self.color_map[step])
                self.painter.drawLine(begin_x, y, end_x, y)

            self.painter.setPen(QColor(0, 0, 0))
            self.painter.drawLine(end_x, mid_y, end_x + 10, mid_y)
            self.painter.drawText(end_x + 20, mid_y, '{}'.format(step))

    def drawPoints(self):
        print(self.bases_map_x, self.bases_map_x + self.bases_map_length, self.bases_map_y, self.bases_map_height)
        bases_map_end_x = self.bases_map_x + self.bases_map_length
        calc_y_array = [y for y in range(self.bases_map_y, self.bases_map_height)]
        calc_y_array.reverse()
        for x in range(self.bases_map_x, bases_map_end_x):
            for y in range(self.bases_map_y, self.bases_map_height):
                calc_x = float((x - self.bases_map_x) / 10.0)
                calc_y = float(calc_y_array[y] / 10.0)
                count = self.calcCoverBaseCount(calc_x, calc_y)
                # print('calcCoverBaseCount :', count)
                self.painter.setPen(self.color_map[count])
                self.painter.drawPoint(x, y)

    def drawXScale(self):
        self.painter.setPen(QColor(0, 0, 0))
        src_y = self.bases_map_height
        dest_y = self.bases_map_height + 20
        step_width = int(self.bases_map_length / 10)

        for step in range(0, 11):
            scale = step * step_width
            x = self.bases_map_x + scale
            self.painter.drawLine(x, src_y, x, dest_y)
            self.painter.drawText(x, dest_y+10, '{}'.format(float(scale/10)))

    def drawYScale(self):
        self.painter.setPen(QColor(0, 0, 0))
        src_x = self.bases_map_x - 20
        dest_x = self.bases_map_x
        step_height = int(self.bases_map_height / 10)

        for step in range(0, 11):
            scale = step * step_height
            y = self.bases_map_y + self.bases_map_height - scale
            self.painter.drawLine(src_x, y, dest_x, y)
            self.painter.drawText(src_x-20, y, '{}'.format(float(scale/10)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    heat_map = FreqHeatMap(81, 42)
    ex = MainWidget(heat_map)
    sys.exit(app.exec_())
