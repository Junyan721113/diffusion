# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog
from PyQt5.QtGui import QIcon
from typing import Union
import cv2
from qfluentwidgets import ScrollArea, PushButton, SettingCard, FluentIconBase, FluentIcon

from image_processor import imageProc


class PushSettingCardStr(SettingCard):

    def __init__(self,
                 icon: Union[str, QIcon, FluentIconBase],
                 title,
                 imagePath=None,
                 parent=None):
        super().__init__(icon, title, "New Simulator", parent)
        self.title = title
        self.startButton = PushButton("开始模拟", self)
        self.stopButton = PushButton("停止模拟", self)
        self.saveButton = PushButton("保存", self)

        self.startButton.setStyleSheet("background: white;")
        self.stopButton.setStyleSheet("background: white;")
        self.saveButton.setStyleSheet("background: white;")

        self.hBoxLayout.addWidget(self.startButton, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.stopButton, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.saveButton, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

        self.startButton.clicked.connect(self.__onStartClicked)
        self.stopButton.clicked.connect(self.__onStopClicked)
        self.saveButton.clicked.connect(self.__onSaveClicked)

        self.imgProc = imageProc(title, imagePath)

    def __onStartClicked(self):
        self.imgProc.running = True
        self.startButton.setStyleSheet("background: lightgreen;")
        self.stopButton.setStyleSheet("background: lightgreen;")
        self.imgProc.runLoop()

    def __onStopClicked(self):
        self.imgProc.running = False
        self.startButton.setStyleSheet("background: white;")
        self.stopButton.setStyleSheet("background: white;")

    def __onSaveClicked(self):
        path, _ = QFileDialog.getSaveFileName(self, "保存为图片", "./", "Image Files (*.bmp)")
        if path == "":
            return
        cv2.imwrite(path, self.imgProc.runImage * 256.0 / self.imgProc.limit)


class TasksInterface(ScrollArea):
    """ Tasks interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.titleLabel = QLabel(self.tr("模拟\nSimulate"), self)
        self.titleLabel.setStyleSheet(
            "color: black; font-family: Cascadia Code, 仿宋; font-size: 32px; font-weight: 600;"
        )
        self.initButton = PushButton("创建模拟", self)
        self.initButton2 = PushButton("从图片创建...", self)
        self.simulatorList = []
        self.__initWidget()

    def __onInitClicked(self):
        self.simulatorList.append(
            PushSettingCardStr(FluentIcon.TAG,
                               "Simulator " + str(len(self.simulatorList)),
                               None, self))
        self.vBoxLayout.addWidget(self.simulatorList[-1])

    def __onInitClicked2(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择图片", "./", "Image Files (*.bmp)")
        if path == "":
            return
        self.simulatorList.append(
            PushSettingCardStr(FluentIcon.TAG,
                               "Simulator " + str(len(self.simulatorList)),
                               path, self))
        self.vBoxLayout.addWidget(self.simulatorList[-1])

    def __initWidget(self):
        self.view.setObjectName('view')
        self.setObjectName('tasksInterface')
        self.titleLabel.setObjectName('tasksLabel')

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(36, 18, 36, 0)
        self.vBoxLayout.setSpacing(18)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(self.initButton, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(self.initButton2, 0, Qt.AlignTop)

        self.initButton.clicked.connect(self.__onInitClicked)
        self.initButton2.clicked.connect(self.__onInitClicked2)
