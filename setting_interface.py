# coding:utf-8
from qfluentwidgets import (SettingCardGroup, PushSettingCard, ScrollArea, Pivot,
                            qrouter)
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog, QVBoxLayout, QStackedWidget

from config import Config


class SettingInterface(ScrollArea):
    """ Setting interface """

    Nav = Pivot

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.scrollWidget = QWidget()
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)

        self.pivot = self.Nav(self)
        self.stackedWidget = QStackedWidget(self)

        # setting label
        self.settingLabel = QLabel(self.tr("设置\nSettings"), self)
        self.settingLabel.setStyleSheet(
            "color: black; font-family: Cascadia Code, 仿宋; font-size: 32px; font-weight: 600;"
        )

        # program group
        self.ProgramGroup = SettingCardGroup(self.tr('程序设置'),
                                             self.scrollWidget)
        self.importConfigCard = PushSettingCard(
            self.tr('导入'), FIF.ADD_TO, self.tr('导入配置'),
            self.tr('选择需要导入的 config.yaml 文件'))

        self.ParamGroup = SettingCardGroup(self.tr("参数设置"), self.scrollWidget)

        self.imagePathCard = PushSettingCard(self.tr('修改'), FIF.IMAGE_EXPORT,
                                             self.tr("图像路径"),
                                             self.tr('选择需要导入的初始图像'))
        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 145, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName('settingInterface')

        # initialize style sheet
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')

        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.settingLabel.move(36, 30)
        # add cards to group
        self.ProgramGroup.addSettingCard(self.importConfigCard)

        self.ParamGroup.addSettingCard(self.imagePathCard)

        self.ProgramGroup.titleLabel.setHidden(True)
        self.ParamGroup.titleLabel.setHidden(True)

        # add items to pivot
        self.addSubInterface(self.ProgramGroup, 'programInterface',
                             self.tr('程序'))
        self.addSubInterface(self.ParamGroup, 'ParamInterface', self.tr('参数'))

        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.ProgramGroup)
        self.pivot.setCurrentItem(self.ProgramGroup.objectName())

        qrouter.setDefaultRouteKey(self.stackedWidget,
                                   self.ProgramGroup.objectName())

        # add setting card group to layout
        self.vBoxLayout.setContentsMargins(36, 10, 36, 0)

    def addSubInterface(self, widget: QLabel, objectName, text):
        widget.setObjectName(objectName)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget))

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())
        qrouter.push(self.stackedWidget, widget.objectName())

    def __onImportConfigCardClicked(self):
        configdir, _ = QFileDialog.getOpenFileName(self, "选取配置文件", "./",
                                                   "Config Files (*.yaml)")
        if (configdir != ""):
            config = Config("./resources/config.example.yaml", "./config.yaml")
            config._load_config(configdir)
            config.save_config()

    def __onImagePathCardClicked(self):
        image_path, _ = QFileDialog.getOpenFileName(self, "选取图片", "",
                                                    "All Files (*)")
        config = Config("./resources/config.example.yaml", "./config.yaml")
        config.set_value("startImage", image_path)
        self.imagePathCard.setContent(image_path)

    def __connectSignalToSlot(self):
        """ connect signal to slot """

        self.importConfigCard.clicked.connect(self.__onImportConfigCardClicked)
        self.imagePathCard.clicked.connect(self.__onImagePathCardClicked)
