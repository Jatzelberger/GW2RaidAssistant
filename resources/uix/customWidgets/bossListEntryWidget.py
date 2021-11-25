from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QLabel
import resources.uix.customWidgets.stylesheets.bossListEntryWidgetStyle as widgetStyle
from resources.backend.bossObject import BossObject


class BossListEntryWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self, parent=None)

        self.widgetWidth = 350
        self.widgetHeight = 50

        self.loadingIconPath = 'resources/graphics/icons/loading_15x15.png'
        self.successIconPath = 'resources/graphics/icons/success_15x15.png'
        self.failIconPath = 'resources/graphics/icons/fail_15x15.png'
        self.errorIconPath = 'resources/graphics/icons/error_15x15.png'
        self.cmIconPath = 'resources/graphics/icons/cm_20x20.png'

        self.bossObject = None

        self.__initWidget()

    def __initWidget(self):
        self.__widgetFrame()
        self.__widgetElements()

    def __widgetFrame(self):
        self.setFixedHeight(self.widgetWidth)
        self.setFixedHeight(self.widgetHeight)

    def __widgetElements(self):
        self.__bossIcon()
        self.__bossName()
        self.__bossTime()
        self.__statusIcon()
        self.__cmIcon()

    def __bossIcon(self):
        size = 40
        bossPixmap = QPixmap('resources/graphics/bosses/loading.png').scaled(size, size)
        self.bossIcon = QLabel(self)
        self.bossIcon.setPixmap(bossPixmap)
        self.bossIcon.setGeometry(5, int((self.height() - size) / 2), size, size)
        self.bossIcon.setStyleSheet(widgetStyle.bossIconStyle())
        self.bossIcon.setToolTip('Loading...')

    def __bossName(self):
        size = (250, 50)
        self.bossName = QLabel(self)
        self.bossName.setText('Loading...')
        self.bossName.setGeometry(55, 6, size[0], size[1])
        self.bossName.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.bossName.setStyleSheet(widgetStyle.bossNameNewStyle())

    def __bossTime(self):
        size = (250, 50)
        self.logTime = QLabel(self)
        self.logTime.setText(datetime.now().strftime('%H:%M'))
        self.logTime.setStyleSheet(widgetStyle.logTimeNewStyle())
        self.logTime.setGeometry(55, 27, size[0], size[1])
        self.logTime.setAlignment(Qt.AlignmentFlag.AlignTop)

    def __statusIcon(self):
        size = 15
        statusPixmap = QPixmap(self.loadingIconPath).scaled(size, size)
        self.statusIcon = QLabel(self)
        self.statusIcon.setPixmap(statusPixmap)
        self.statusIcon.setToolTip('Loading...')
        self.statusIcon.setGeometry(30, 30, size, size)
        self.statusIcon.setStyleSheet(widgetStyle.statusIconStyle())

    def __cmIcon(self):
        size = 20
        cmPixmap = QPixmap(self.cmIconPath).scaled(size, size)
        self.challengeMoteIcon = QLabel(self)
        self.challengeMoteIcon.setPixmap(cmPixmap)
        self.challengeMoteIcon.setGeometry(5, 30, size, size)
        self.challengeMoteIcon.setStyleSheet(widgetStyle.statusIconStyle())
        self.challengeMoteIcon.setToolTip('Challenge Mote')
        self.challengeMoteIcon.hide()

    def updateData(self, bossObject: BossObject):
        self.bossObject = bossObject
        if self.bossObject is None:
            print('tried to update widget without setting data' + str(self))
        else:
            size = 40
            bossPixmap = QPixmap(self.bossObject.icon).scaled(size, size)
            self.bossIcon.setPixmap(bossPixmap)
            self.bossIcon.setToolTip(self.bossObject.name)

            self.bossName.setText(self.bossObject.name)
            self.bossName.setStyleSheet(
                widgetStyle.bossNameOldStyle() if self.bossObject.old else widgetStyle.bossNameNewStyle()
            )

            self.logTime.setText(
                self.bossObject.time.strftime(
                    '%H:%M' if self.bossObject.time.date() == datetime.today().date() else '%H:%M  %a, %d.%m.%Y'
                )
            )
            self.logTime.setStyleSheet(
                widgetStyle.logTimeOldStyle() if self.bossObject.old else widgetStyle.logTimeNewStyle()
            )

            size = 15
            if self.bossObject.success is not None:
                statusPixmap = QPixmap(
                    self.successIconPath if self.bossObject.success else self.failIconPath
                ).scaled(size, size)
                self.statusIcon.setPixmap(statusPixmap)
                self.statusIcon.setToolTip('Success' if self.bossObject.success else 'Fail')

            if self.bossObject.cm:
                # self.challengeMoteIcon.show()
                self.bossName.setText(self.bossName.text() + ' CM')

    def getBossObject(self):
        return self.bossObject

    def setError(self, code: str):
        size = 15
        statusPixmap = QPixmap(self.errorIconPath).scaled(size, size)
        self.statusIcon.setPixmap(statusPixmap)
        self.statusIcon.setToolTip('ERROR: ' + code)
