from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSize

from qfluentwidgets import NavigationItemPosition, MSFluentWindow, SplashScreen, setThemeColor, NavigationBarPushButton, toggleTheme, setTheme, darkdetect, Theme
from qfluentwidgets import FluentIcon as FIF

from home_interface import HomeInterface
from setting_interface import SettingInterface
from tasks_interface import TasksInterface


class MainWindow(MSFluentWindow):

    def __init__(self):
        super().__init__()
        setThemeColor('#f18cb9')
        setTheme(Theme.DARK if darkdetect.theme() == 'Dark' else Theme.LIGHT)

        self.initWindow()

        # create sub interface
        self.homeInterface = HomeInterface(self)
        self.tasksInterface = TasksInterface(self)
        self.settingInterface = SettingInterface(self)

        self.initNavigation()
        self.splashScreen.finish()

    def initNavigation(self):
        self.stackedWidget.setStyleSheet("border: 0px;")
        # add navigation items
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('主页'))
        self.addSubInterface(self.tasksInterface, FIF.LABEL, self.tr('模拟'))

        # self.navigationInterface.addWidget(
        #     'themeButton',
        #     NavigationBarPushButton(FIF.BRUSH, '主题', isSelectable=False),
        #     self.toggleTheme, NavigationItemPosition.BOTTOM)

        self.addSubInterface(self.settingInterface,
                             FIF.SETTING,
                             self.tr('设置'),
                             position=NavigationItemPosition.BOTTOM)

    def initWindow(self):
        # 禁用最大化
        self.titleBar.maxBtn.setHidden(True)
        self.titleBar.maxBtn.setDisabled(True)
        self.titleBar.setDoubleClickEnabled(False)
        self.setResizeEnabled(False)

        self.resize(960, 780)
        self.setWindowIcon(QIcon('./resources/icon.jpg'))
        self.setWindowTitle("Diffusion Simulator")

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(128, 128))
        self.splashScreen.raise_()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def toggleTheme(self):
        toggleTheme(save=False)
