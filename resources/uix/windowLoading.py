import sys
import resources.uix.stylesheets.windowLoadingStyle as windowStyle

from PyQt6.QtCore import QThreadPool, Qt
from PyQt6.QtGui import QGuiApplication, QIcon, QPixmap
from PyQt6.QtWidgets import QWidget, QLabel, QGraphicsDropShadowEffect, QProgressBar
from resources.backend.configObject import ConfigObject
from resources.backend.threads.configThread import ConfigThread
from resources.uix.windowMain import MainWindow


class WindowLoading(QWidget):
    def __init__(self):
        super().__init__()

        self.windowWidth = 500
        self.windowHeight = 300
        self.windowName = 'GW2RaidAssistant'
        self.frameShadowSize = 8

        self.config = ConfigObject()  # default data object
        self.bossStorage = {}  # storage for stored logs
        self.threadPool = QThreadPool()

        self.initUI()
        self.initWidget()
        self.initThread()

    # # # UI INIT
    def initUI(self):
        self.windowSize()
        self.windowPosition()
        self.windowAttributes()
        self.windowStyle()
        self.windowContainer()
        self.windowShadow()

    def windowSize(self):
        """ Set fixed window size """
        self.setFixedWidth(self.windowWidth)
        self.setFixedHeight(self.windowHeight)

    def windowPosition(self):
        """ Open window in center of screen """
        monitor_resolution = QGuiApplication.primaryScreen().geometry()
        x_value = int((monitor_resolution.width() - self.frameSize().width() + self.frameShadowSize) / 2)
        y_value = int((monitor_resolution.height() - self.frameSize().height() + self.frameShadowSize) / 2)
        self.move(x_value, y_value)

    def windowAttributes(self):
        """ Set window name and icon """
        self.setWindowTitle(self.windowName)
        self.setWindowIcon(QIcon('resources/graphics/uix/titleImage_500x500.png'))

    def windowStyle(self):
        """ Set window style """
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)  # remove default title bar
        self.setWindowFlag(Qt.WindowType.SplashScreen, True)  # hide from taskbar
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # Make window translucent (shadow container)

    def windowContainer(self):
        """ Create window container """
        self.container = QLabel(self)
        self.container.setGeometry(
            0,
            0,
            self.windowWidth - self.frameShadowSize,
            self.windowHeight - self.frameShadowSize,
        )
        self.container.setStyleSheet(windowStyle.windowContainerStyle())

    def windowShadow(self):
        """ Create window shadow effect """
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(self.frameShadowSize)
        shadow.setXOffset(1)
        shadow.setYOffset(1)
        self.container.setGraphicsEffect(shadow)

    # # # WIDGET INIT
    def initWidget(self):
        self.titleImageWidget()
        self.titleTextWidget()
        self.authorTextWidget()
        self.progressBarWidget()

    def titleImageWidget(self):
        """ show title image """
        size = (200, 200)
        imagePixmap = QPixmap('resources/graphics/uix/titleImage_500x500.png').scaled(size[0], size[1])
        titleImage = QLabel(self.container)
        titleImage.setGeometry(int((self.container.width() - size[0]) / 2), 20, size[0], size[1])
        titleImage.setStyleSheet(windowStyle.titleImageWidgetStyle())
        titleImage.setPixmap(imagePixmap)

    def titleTextWidget(self):
        """ show app name text """
        titleText = QLabel(self.container)
        titleText.setText('GW2RaidAssistant')
        titleText.setGeometry(0, 140, self.container.width(), 40)
        titleText.setStyleSheet(windowStyle.titleTextWidgetStyle())
        titleText.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def authorTextWidget(self):
        """ show app author text """
        authorText = QLabel(self.container)
        authorText.setText('by Jatzelberger')
        authorText.setGeometry(219, 178, 200, 30)
        authorText.setStyleSheet(windowStyle.authorTextWidgetStyle())
        authorText.setAlignment(Qt.AlignmentFlag.AlignRight)

    def progressBarWidget(self):
        """ initiate progress bar with 0 value """
        size = (self.container.width(), 10)
        self.progressBar = QProgressBar(self.container)
        self.progressBar.setTextVisible(False)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setGeometry(0, self.container.height() - size[1], size[0], size[1])
        self.progressBar.setStyleSheet(windowStyle.progressBarWidgetStyle())
        self.progressBar.setValue(0)

    # # # THREAD INIT
    def initThread(self):
        configThread = ConfigThread(self.config)
        configThread.signal.newProgress.connect(self.configThreadProgressAction)
        configThread.signal.newLogStorage.connect(self.configThreadBossStorageAction)
        configThread.signal.newEndSignal.connect(self.configThreadEndAction)
        self.threadPool.start(configThread)

    # # # BACKEND FUNCTIONS
    def configThreadProgressAction(self, value):
        """ sets new value on progress bar """
        self.progressBar.setValue(value)

    def configThreadBossStorageAction(self, value):
        """ sets boss storage dict when read from file """
        self.bossStorage = value

    def configThreadEndAction(self, value):
        """ handles actions on loading end """
        if value:
            self.window = MainWindow(self.config, self.bossStorage)
            self.window.show()
            self.hide()
        else:
            self.threadPool.clear()  # stops configThread if it should still be running
            sys.exit()
