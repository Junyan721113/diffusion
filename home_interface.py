# coding:utf-8
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QPainterPath
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsDropShadowEffect

from qfluentwidgets import ScrollArea


class BannerWidget(QWidget):
    """ Banner widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(450)

        self.vBoxLayout = QVBoxLayout(self)
        self.galleryLabel = QLabel(f'扩散模拟器\nDiffusion Simulator', self)
        self.galleryLabel.setStyleSheet("color: white; font-family: Cascadia Code, 仿宋; font-size: 32px; font-weight: 600;")

        # 创建阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)  # 阴影模糊半径
        shadow.setColor(Qt.black)  # 阴影颜色
        shadow.setOffset(1.2, 1.2)     # 阴影偏移量

        # 将阴影效果应用于小部件
        self.galleryLabel.setGraphicsEffect(shadow)

        self.banner = QPixmap('./resources/background.bmp')

        self.galleryLabel.setObjectName('galleryLabel')

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(25, 20, 0, 0)
        self.vBoxLayout.addWidget(self.galleryLabel)
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)


    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        w, h = self.width(), 450
        path.addRoundedRect(QRectF(0, 0, w, h), 10, 10)
        path = path.simplified()

        # Calculate the required height for maintaining image aspect ratio
        image_height = self.width() * self.banner.height() // self.banner.width()

        # draw banner image with aspect ratio preservation
        pixmap = self.banner.scaled(self.width(), image_height, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        painter.fillPath(path, QBrush(pixmap))


class HomeInterface(ScrollArea):
    """ Home interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.banner = BannerWidget(self)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__initWidget()

    def __initWidget(self):
        self.view.setObjectName('view')
        self.setObjectName('homeInterface')

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.addWidget(self.banner)
