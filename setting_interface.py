# coding:utf-8
from qfluentwidgets import (SettingCardGroup, PushSettingCard, ScrollArea, Pivot, MessageBox, LineEdit,
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
        self.limitCard = PushSettingCard(self.tr('修改'), FIF.ADD_TO,
                                         self.tr("默认极限值"),
                                         self.tr('系统的浓度值将限制在 0 到此值之间'))
        self.alphaCard = PushSettingCard(self.tr('修改'), FIF.ADD_TO,
                                         self.tr("扩散速度"),
                                         self.tr('系统中物质的扩散速度'))
        self.veloxCard = PushSettingCard(self.tr('修改'), FIF.ADD_TO,
                                         self.tr("介质横向速度"),
                                         self.tr('介质的横向速度'))
        self.veloyCard = PushSettingCard(self.tr('修改'), FIF.ADD_TO,
                                         self.tr("介质纵向速度"),
                                         self.tr('介质的纵向速度'))
        self.kappaCard = PushSettingCard(self.tr('修改'), FIF.ADD_TO,
                                         self.tr("反应常数"),
                                         self.tr('化学反应 R + G = B 的反应常数'))
        self.mlengCard = PushSettingCard(self.tr('修改'), FIF.ADD_TO,
                                         self.tr("空间比例尺"),
                                         self.tr('每像素的实际长度'))
        self.mtimeCard = PushSettingCard(self.tr('修改'), FIF.ADD_TO,
                                         self.tr("时间比例尺"),
                                         self.tr('每帧的实际时间'))

        self.RenderGroup = SettingCardGroup(self.tr("渲染设置"), self.scrollWidget)

        self.doLogCard = PushSettingCard(self.tr('修改'), FIF.ADD_TO,
                                         self.tr("对数渲染"),
                                         self.tr('是否对图像进行对数处理，以更好模拟人眼对亮度的感知'))
        self.p2drateCard = PushSettingCard(self.tr('修改'), FIF.ADD_TO,
                                           self.tr("二维图表渲染速度"),
                                           self.tr('二维图表两次渲染之间的帧数间隔'))
        self.p3drateCard = PushSettingCard(self.tr('修改'), FIF.ADD_TO,
                                           self.tr("三维图表渲染速度"),
                                           self.tr('三维图表两次渲染之间的帧数间隔'))
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
        self.ParamGroup.addSettingCard(self.limitCard)
        self.ParamGroup.addSettingCard(self.alphaCard)
        self.ParamGroup.addSettingCard(self.veloxCard)
        self.ParamGroup.addSettingCard(self.veloyCard)
        self.ParamGroup.addSettingCard(self.kappaCard)
        self.ParamGroup.addSettingCard(self.mlengCard)
        self.ParamGroup.addSettingCard(self.mtimeCard)

        self.RenderGroup.addSettingCard(self.doLogCard)
        self.RenderGroup.addSettingCard(self.p2drateCard)
        self.RenderGroup.addSettingCard(self.p3drateCard)

        self.ProgramGroup.titleLabel.setHidden(True)
        self.ParamGroup.titleLabel.setHidden(True)
        self.RenderGroup.titleLabel.setHidden(True)

        # add items to pivot
        self.addSubInterface(self.ProgramGroup, 'programInterface',
                             self.tr('程序'))
        self.addSubInterface(self.ParamGroup, 'ParamInterface', self.tr('参数'))
        self.addSubInterface(self.RenderGroup, 'RenderInterface', self.tr('渲染'))

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

    def __convertGenerator(self, type):
        def __convert(value):
            if type == "bool":
                return value == "True"
            elif type == "int":
                return int(value)
            elif type == "float":
                return float(value)
            else:
                return value
        return __convert

    def __onCardClickedGenerator(self, card: PushSettingCard, configname: str, type: str = "float"):
        ledit = LineEdit(card)
        card.hBoxLayout.addWidget(ledit, 0, Qt.AlignRight)
        card.hBoxLayout.addSpacing(10)
        card.hBoxLayout.addWidget(card.button, 0, Qt.AlignRight)
        card.hBoxLayout.addSpacing(16)
        config = Config("./resources/config.example.yaml", "./config.yaml")
        ledit.setText(str(config.get_value(configname)))
        def __onCardClicked():
            if ledit.text():
                config.set_value(configname, self.__convertGenerator(type)(ledit.text()))
                ledit.setText(str(config.get_value(configname)))
        return __onCardClicked


    def __connectSignalToSlot(self):
        """ connect signal to slot """

        self.importConfigCard.clicked.connect(self.__onImportConfigCardClicked)
        self.imagePathCard.clicked.connect(self.__onImagePathCardClicked)
        self.doLogCard.clicked.connect(self.__onCardClickedGenerator(self.doLogCard, "doLog", "bool"))
        self.limitCard.clicked.connect(self.__onCardClickedGenerator(self.limitCard, "limit"))
        self.alphaCard.clicked.connect(self.__onCardClickedGenerator(self.alphaCard, "real_alpha"))
        self.veloxCard.clicked.connect(self.__onCardClickedGenerator(self.veloxCard, "real_vx"))
        self.veloyCard.clicked.connect(self.__onCardClickedGenerator(self.veloyCard, "real_vy"))
        self.kappaCard.clicked.connect(self.__onCardClickedGenerator(self.kappaCard, "K"))
        self.mlengCard.clicked.connect(self.__onCardClickedGenerator(self.mlengCard, "L"))
        self.mtimeCard.clicked.connect(self.__onCardClickedGenerator(self.mtimeCard, "T"))
        self.p2drateCard.clicked.connect(self.__onCardClickedGenerator(self.p2drateCard, "p2drate", "int"))
        self.p3drateCard.clicked.connect(self.__onCardClickedGenerator(self.p3drateCard, "p3drate", "int"))
