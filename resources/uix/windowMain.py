from PyQt6.QtCore import QThreadPool, Qt, QSize, QEvent
from PyQt6.QtGui import QGuiApplication, QIcon, QAction
from PyQt6.QtWidgets import QMainWindow, QLabel, QGraphicsDropShadowEffect, QPushButton, QListWidget, QScrollBar, \
    QAbstractItemView, QListWidgetItem, QMenu, QLineEdit, QCheckBox, QComboBox, QFileDialog, QSpinBox
from os import system as os_system
from sys import exit as sys_exit
from subprocess import Popen as sub_Popen
from webbrowser import open as web_open
from resources.backend.configObject import ConfigObject
from resources.backend.bossObject import BossObject
from resources.backend.threads.fileThread import FileServiceThread
from resources.backend.threads.uploadThread import UploadServiceThread
from resources.backend.threads.discordThread import DiscordServiceThread
from resources.backend.threads.saveConfigThread import SaveConfigThread
from resources.uix.customWidgets.bossListEntryWidget import BossListEntryWidget
import resources.uix.stylesheets.windowMainStyle as windowStyle


class MainWindow(QMainWindow):
    def __init__(self, configObject: ConfigObject, bossStorage: dict):
        super().__init__()

        self.configObject = configObject  # configObject
        self.bossStorage = bossStorage  # old logs from bossStorage

        self.windowWidth = 400
        self.windowHeight = 600
        self.windowName = 'GW2RaidAssistant'
        self.frameShadowSize = 8
        self.titleBarHeight = 28
        self.sideBarWidth = 34

        self.threadPool = QThreadPool()
        self.move_offset = None  # init for mouse move events
        self.activeTab = 0  # 0: HOME, 1: DISCORD, 2: SETTINGS
        self.automaticPosting = False  # default: automatic webhook posting disabled

        self.initUI()
        self.initWidget()
        self.setActiveTab(0)  # set tab to init active tab
        self.initThread()

    # # # CUSTOM MOUSE EVENTS
    def mousePressEvent(self, event):
        if event.pos().y() <= self.titleBarHeight \
                and event.pos().x() <= (self.width() - self.frameShadowSize) \
                and event.button() == Qt.MouseButton.LeftButton:
            self.move_offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.move_offset is not None and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.pos() - self.move_offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.move_offset = None
        super().mouseReleaseEvent(event)

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
        self.setWindowIcon(QIcon('resources/graphics/uix/titleimage_500x500.png'))

    def windowStyle(self):
        """ Set window style """
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)  # remove default title bar
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
        self.sideBar()
        self.titleBar()  # titleBar has to be on top of sideBar for shadow effect
        self.tabContainer()

    # # Title Bar Widget
    def titleBar(self):
        self.titleBarBackground()
        self.titleBarCloseButton()
        self.titleBarMinimizeButton()

    def titleBarBackground(self):
        """ Title bar background and application name """
        background = QLabel(self.container)
        background.setGeometry(0, 0, self.container.width(), self.titleBarHeight)
        background.setStyleSheet(windowStyle.titleBarBackgroundStyle())
        background.setAlignment(Qt.AlignmentFlag.AlignCenter)
        background.setText(self.windowName)

        shadow = QGraphicsDropShadowEffect()  # shadow effect
        shadow.setBlurRadius(5)
        shadow.setXOffset(0)
        shadow.setYOffset(1)
        background.setGraphicsEffect(shadow)

    def titleBarCloseButton(self):
        """ New window close button """
        closeButton = QPushButton(self.container)
        closeButton.setGeometry(self.container.width() - 24, 4, 20, 20)
        closeButton.setStyleSheet(windowStyle.titleBarCloseButtonStyle())
        closeButton.setIcon(QIcon('resources/graphics/icons/close_200x200.png'))
        closeButton.setIconSize(QSize(12, 12))
        closeButton.setToolTip('close application')
        closeButton.clicked.connect(self.titleBarCloseButtonAction)

    def titleBarMinimizeButton(self):
        """ New window minimize button """
        minimizeButton = QPushButton(self.container)
        minimizeButton.setGeometry(self.container.width() - 44, 4, 20, 20)
        minimizeButton.setStyleSheet(windowStyle.titleBarMinimizeButtonStyle())
        minimizeButton.setIcon(QIcon('resources/graphics/icons/minimize_200x200.png'))
        minimizeButton.setIconSize(QSize(12, 12))
        minimizeButton.setToolTip('minimize application')
        minimizeButton.clicked.connect(self.titleBarMinimizeButtonAction)

    # # Side Bar Widget
    def sideBar(self):
        self.sideBarBackground()
        self.sideBarHomeButton()
        self.sideBarDiscordButton()
        self.sideBarSettingsButton()
        self.sideBarGitHubButton()

    def sideBarBackground(self):
        """ Side bar background """
        background = QLabel(self.container)
        background.setGeometry(0, self.titleBarHeight, self.sideBarWidth, self.container.height() - self.titleBarHeight)
        background.setStyleSheet(windowStyle.sideBarBackgroundStyle())

    def sideBarHomeButton(self):
        """ Button to enter HOME tab """
        self.sideBarHomeBtn = QPushButton(self.container)
        self.sideBarHomeBtn.setGeometry(0, 135, self.sideBarWidth, 80)
        self.sideBarHomeBtn.setStyleSheet(windowStyle.sideBarButtonInactiveStyle())
        self.sideBarHomeBtn.setIcon(QIcon('resources/graphics/uix/hometab_50x200.png'))
        self.sideBarHomeBtn.setIconSize(QSize(20, 80))
        self.sideBarHomeBtn.clicked.connect(self.sideBarHomeButtonAction)

    def sideBarDiscordButton(self):
        """ Button to enter DISCORD tab """
        self.sideBarDiscordBtn = QPushButton(self.container)
        self.sideBarDiscordBtn.setGeometry(
            0,
            self.sideBarHomeBtn.y() + self.sideBarHomeBtn.height(),
            self.sideBarWidth,
            100
        )
        self.sideBarDiscordBtn.setStyleSheet(windowStyle.sideBarButtonInactiveStyle())
        self.sideBarDiscordBtn.setIcon(QIcon('resources/graphics/uix/discordtab_50x200.png'))
        self.sideBarDiscordBtn.setIconSize(QSize(20, 80))
        self.sideBarDiscordBtn.clicked.connect(self.sideBarDiscordButtonAction)

    def sideBarSettingsButton(self):
        """ Button to enter SETTINGS tab """
        self.sideBarSettingsBtn = QPushButton(self.container)
        self.sideBarSettingsBtn.setGeometry(
            0,
            self.sideBarDiscordBtn.y() + self.sideBarDiscordBtn.height(),
            self.sideBarWidth,
            105
        )
        self.sideBarSettingsBtn.setStyleSheet(windowStyle.sideBarButtonInactiveStyle())
        self.sideBarSettingsBtn.setIcon(QIcon('resources/graphics/uix/settingstab_50x200.png'))
        self.sideBarSettingsBtn.setIconSize(QSize(20, 80))
        self.sideBarSettingsBtn.clicked.connect(self.sideBarSettingsButtonAction)

    def sideBarGitHubButton(self):
        """ Button to open browser and navigate to authors GitHub page """
        gitHubButton = QPushButton(self.container)
        gitHubButton.setGeometry(5, self.container.height() - 29, 24, 24)
        gitHubButton.setStyleSheet(windowStyle.sideBarGithubButtonStyle())
        gitHubButton.setIcon(QIcon('resources/graphics/icons/github_200x200.png'))
        gitHubButton.setIconSize(QSize(15, 15))
        gitHubButton.setToolTip('GitHub: Jatzelberger')
        gitHubButton.clicked.connect(self.sideBarGitHubButtonAction)

    # # Tab container
    def tabContainer(self):
        self.tabContainerHome()
        self.tabContainerDiscord()
        self.tabContainerSettings()
        self.tabContent()

    def tabContainerHome(self):
        """ Creates widget container for HOME tab """
        self.homeContainer = QLabel(self.container)
        self.homeContainer.setGeometry(
            self.sideBarWidth,
            self.titleBarHeight,
            self.container.width() - self.sideBarWidth,
            self.container.height() - self.titleBarHeight
        )
        self.homeContainer.setStyleSheet(windowStyle.tabContainerBackgroundStyle())

    def tabContainerDiscord(self):
        """ Creates widget container for DISCORD tab """
        self.discordContainer = QLabel(self.container)
        self.discordContainer.setGeometry(
            self.sideBarWidth,
            self.titleBarHeight,
            self.container.width() - self.sideBarWidth,
            self.container.height() - self.titleBarHeight
        )
        self.discordContainer.setStyleSheet(windowStyle.tabContainerBackgroundStyle())

    def tabContainerSettings(self):
        """ Creates widget container for SETTINGS tab """
        self.settingsContainer = QLabel(self.container)
        self.settingsContainer.setGeometry(
            self.sideBarWidth,
            self.titleBarHeight,
            self.container.width() - self.sideBarWidth,
            self.container.height() - self.titleBarHeight
        )
        self.settingsContainer.setStyleSheet(windowStyle.tabContainerBackgroundStyle())

    # # Tab contents
    def tabContent(self):
        self.tabHome()
        self.tabDiscord()
        self.tabSettings()

    # Home Tab
    def tabHome(self):
        self.tabHomeBossList()
        self.tabHomeStartWebhookButton()
        self.tabHomeURLTextBox()
        self.tabHomeDiscordPostButton()

    def tabHomeBossList(self):
        """ Boss list which shows logs """
        self.bossList = QListWidget(self.homeContainer)
        self.bossList.setGeometry(8, 8, self.homeContainer.width() - 16, self.homeContainer.height() - 48)
        self.bossList.setStyleSheet(windowStyle.bossListStyle())
        self.bossList.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.bossList.installEventFilter(self)  # event filter for right click context menu

        customScrollBar = QScrollBar()
        customScrollBar.setStyleSheet(windowStyle.customScrollBarStyle())
        self.bossList.setVerticalScrollBar(customScrollBar)
        self.bossList.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.bossList.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.bossList.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

    def tabHomeBossListContextMenu(self, source, event):
        """ Right click context menu on bossListElements """
        contextMenu = QMenu(self)
        contextMenu.setStyleSheet(windowStyle.bossListContextMenuStyle())

        copyURLButton = QAction('Copy URL', self)
        copyURLButton.triggered.connect(self.bossListContextMenuCopyURLAction)
        copyURLButton.setIcon(QIcon('resources/graphics/icons/copy_48x48.png'))
        if self.bossList.itemWidget(source.itemAt(event.pos())).getBossObject().url != '':  # only if log is uploaded
            contextMenu.addAction(copyURLButton)

        openInBrowserButton = QAction('Open in Browser', self)
        openInBrowserButton.triggered.connect(self.bossListContextMenuOpenBrowserAction)
        openInBrowserButton.setIcon(QIcon('resources/graphics/icons/browser_48x48.png'))
        if self.bossList.itemWidget(source.itemAt(event.pos())).getBossObject().url != '':  # only if log is uploaded
            contextMenu.addAction(openInBrowserButton)

        openInExplorerButton = QAction('Open in Explorer', self)
        openInExplorerButton.setIcon(QIcon('resources/graphics/icons/explorer_48x48.png'))
        openInExplorerButton.triggered.connect(self.bossListContextMenuOpenExplorerAction)
        contextMenu.addAction(openInExplorerButton)

        contextMenu.exec(event.globalPos())  # open menu at mouse position

    def tabHomeStartWebhookButton(self):
        """ starting button for automatic discord posting"""
        self.startWebhookButton = QPushButton('START', self.homeContainer)
        self.startWebhookButton.setGeometry(self.homeContainer.width() - 75, self.homeContainer.height() - 32, 67, 24)
        self.startWebhookButton.setIcon(QIcon('resources/graphics/icons/start_48x48.png'))
        self.startWebhookButton.setIconSize(QSize(20, 20))
        self.startWebhookButton.setStyleSheet(windowStyle.tabHomeStartWebhookButtonStyle())
        self.startWebhookButton.clicked.connect(self.tabHomeStartWebhookButtonAction)
        self.startWebhookButton.setToolTip('start automatic discord posting')

    def tabHomeURLTextBox(self):
        """ textbox for custom postings by dps.report url """
        self.homeURLTextBox = QLineEdit('', self.homeContainer)
        self.homeURLTextBox.setPlaceholderText('dps.report URL')
        self.homeURLTextBox.setStyleSheet(windowStyle.tabHomeURLTextBoxStyle())
        self.homeURLTextBox.setGeometry(
            8,
            self.homeContainer.height() - 32,
            self.startWebhookButton.x() - 36,
            24
        )

        clearTextButton = QPushButton(self.homeContainer)
        clearTextButton.setGeometry(
            self.homeURLTextBox.width() - 14,
            self.homeContainer.height() - 30,
            20,
            20
        )
        clearTextButton.setStyleSheet(windowStyle.tabHomeURLTextBoxDeleteButtonStyle())
        clearTextButton.setIcon(QIcon('resources/graphics/icons/close_200x200.png'))
        clearTextButton.setIconSize(QSize(8, 8))
        clearTextButton.clicked.connect(self.tabHomeTextBoxDeleteButtonAction)

    def tabHomeDiscordPostButton(self):
        """ Button to post selected log or log by permalink on discord """
        button = QPushButton('', self.homeContainer)
        button.setGeometry(
            self.homeURLTextBox.x() + self.homeURLTextBox.width() - 1,
            self.homeContainer.height() - 32,
            24,
            24
        )
        button.setStyleSheet(windowStyle.tabHomeDiscordPostButtonStyle())
        button.setIcon(QIcon('resources/graphics/icons/discord_200x200.png'))
        button.setIconSize(QSize(18, 18))
        button.setToolTip('post URL or selected log on discord')
        button.clicked.connect(self.tabHomeDiscordPostButtonAction)
        # if int(self.config.selectedServer) == -1:
        #    button.setDisabled(True)

    # Discord Tab
    def tabDiscord(self):
        self.tabDiscordBossListHeader()
        self.tabDiscordBossList()
        self.tabDiscordDisplayName()
        self.tabDiscordServerListHeader()
        self.tabDiscordServerList()
        self.tabDiscordServerListAddButton()
        self.tabDiscordServerListRemoveButton()
        self.tabDiscordServerListPopup()
        self.tabDiscordApplyButton()
        self.tabDiscordCancelButton()
        self.tabDiscordOkButton()

    def tabDiscordBossListHeader(self):
        header = QLabel(self.discordContainer)
        header.setGeometry(8, 6, 200, 24)
        header.setText('Enabled Bosses')
        header.setStyleSheet(windowStyle.tabDiscordHeaderTextStyle())

    def tabDiscordBossList(self):
        """ creates empty boss selection list """
        self.enabledBossesList = QListWidget(self.discordContainer)
        self.enabledBossesList.setGeometry(8, 32, self.discordContainer.width() - 16, 300)
        self.enabledBossesList.setStyleSheet(windowStyle.tabDiscordEnabledBossesListStyle())
        self.enabledBossesList.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        customScrollBar = QScrollBar()
        customScrollBar.setStyleSheet(windowStyle.customScrollBarStyle())
        self.enabledBossesList.setVerticalScrollBar(customScrollBar)
        self.enabledBossesList.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.enabledBossesList.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.enabledBossesList.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

    def tabDiscordServerListHeader(self):
        header = QLabel(self.discordContainer)
        header.setGeometry(8, self.enabledBossesList.y() + self.enabledBossesList.height() + 8, 200, 24)
        header.setText('Webhook')
        header.setStyleSheet(windowStyle.tabDiscordHeaderTextStyle())

    def tabDiscordDisplayName(self):
        """ text box and label to change display name """
        label = QLabel(self.discordContainer)
        label.setGeometry(8, self.enabledBossesList.y() + self.enabledBossesList.height() + 34, 100, 24)
        label.setText('Display Name:')
        label.setStyleSheet('color: #2A3241, background-color: rgba(0, 0, 0, 0%)')

        self.webhookDisplayName = QLineEdit(self.discordContainer)
        self.webhookDisplayName.setGeometry(
            90,
            self.enabledBossesList.y() + self.enabledBossesList.height() + 34,
            self.discordContainer.width() - 98,
            24,
        )
        self.webhookDisplayName.setStyleSheet(windowStyle.tabDiscordDisplayNameEditStyle())
        self.webhookDisplayName.setPlaceholderText('display name (leave empty for char name)')

    def tabDiscordServerList(self):
        """ create webhook server list """
        self.serverList = QComboBox(self.discordContainer)
        self.serverList.setGeometry(
            8,
            self.enabledBossesList.y() + self.enabledBossesList.height() + 62,
            self.discordContainer.width() - 152,
            24
        )
        self.serverList.setStyleSheet(windowStyle.tabDiscordServerTable())
        self.serverList.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.serverList.setPlaceholderText('select webhook')

    def tabDiscordServerListAddButton(self):
        """ creates button to open popup for new webhooks """
        button = QPushButton(self.discordContainer)
        button.setGeometry(
            self.serverList.width() + 16,
            self.serverList.y(),
            60,
            24
        )
        button.setStyleSheet(windowStyle.tabDiscordWhiteButtonStyle())
        button.setText('Add')
        button.clicked.connect(self.tabDiscordServerListAddButtonAction)

    def tabDiscordServerListPopup(self):
        """ Creates new webhook popup """
        self.serverListAddPopup = QLabel(self.discordContainer)
        self.serverListAddPopup.setGeometry(
            8,
            self.serverList.y() + 28,
            self.discordContainer.width() - 16,
            32,
        )
        self.serverListAddPopup.setStyleSheet(windowStyle.tabDiscordServerListPopupStyle())

        self.serverListNameEdit = QLineEdit(self.serverListAddPopup)
        self.serverListNameEdit.setGeometry(4, 4, 120, 24)
        self.serverListNameEdit.setPlaceholderText('name')

        self.serverListURLEdit = QLineEdit(self.serverListAddPopup)
        self.serverListURLEdit.setGeometry(128, 4, self.serverListAddPopup.width() - 170, 24)
        self.serverListURLEdit.setPlaceholderText('url')

        serverListAddOKButton = QPushButton(self.serverListAddPopup)
        serverListAddOKButton.setGeometry(self.serverListAddPopup.width() - 38, 4, 34, 24)
        serverListAddOKButton.setStyleSheet(windowStyle.tabDiscordGreenButtonStyle())
        serverListAddOKButton.setText('OK')
        serverListAddOKButton.clicked.connect(self.tabDiscordServerListAddAction)

        self.serverListAddPopup.hide()

    def tabDiscordServerListRemoveButton(self):
        """ Creates button to remove webhooks """
        button = QPushButton(self.discordContainer)
        button.setGeometry(
            self.serverList.width() + 84,
            self.serverList.y(),
            60,
            24
        )
        button.setStyleSheet(windowStyle.tabDiscordWhiteButtonStyle())
        button.setText('Remove')
        button.clicked.connect(self.tabDiscordServerListRemoveButtonAction)

    def tabDiscordApplyButton(self):
        """ create apply settings button for discord tab """
        self.tabDiscordApplyBtn = QPushButton(self.discordContainer)
        self.tabDiscordApplyBtn.setGeometry(
            self.discordContainer.width() - 75,
            self.discordContainer.height() - 32,
            67,
            24,
        )
        self.tabDiscordApplyBtn.setStyleSheet(windowStyle.tabDiscordWhiteButtonStyle())
        self.tabDiscordApplyBtn.setText('Apply')
        self.tabDiscordApplyBtn.clicked.connect(self.tabDiscordApplyButtonAction)

    def tabDiscordCancelButton(self):
        """ create cancel settings button for discord tab """
        self.tabDiscordCancelBtn = QPushButton(self.discordContainer)
        self.tabDiscordCancelBtn.setGeometry(
            self.tabDiscordApplyBtn.x() - 75,
            self.discordContainer.height() - 32,
            67,
            24,
        )
        self.tabDiscordCancelBtn.setStyleSheet(windowStyle.tabDiscordWhiteButtonStyle())
        self.tabDiscordCancelBtn.setText('Cancel')
        self.tabDiscordCancelBtn.clicked.connect(self.tabDiscordCancelButtonAction)

    def tabDiscordOkButton(self):
        """ create ok settings button for discord tab """
        button = QPushButton(self.discordContainer)
        button.setGeometry(
            self.tabDiscordCancelBtn.x() - 75,
            self.discordContainer.height() - 32,
            67,
            24,
        )
        button.setStyleSheet(windowStyle.tabDiscordGreenButtonStyle())
        button.setText('OK')
        button.clicked.connect(self.tabDiscordOkButtonAction)

    # Settings Tab
    def tabSettings(self):
        self.tabSettingsHeaderFolder()
        self.tabSettingsRootPath()
        self.tabSettingsPollingRate()
        self.tabSettingsHeaderReport()
        self.tabSettingsUserToken()
        self.tabSettingsAnonymousCheckBox()
        self.tabSettingsApplyButton()
        self.tabSettingsCancelButton()
        self.tabSettingsOkButton()

    def tabSettingsHeaderFolder(self):
        """ folder settings label """
        header = QLabel(self.settingsContainer)
        header.setGeometry(8, 6, 200, 24)
        header.setText('Folder Settings')
        header.setStyleSheet(windowStyle.tabDiscordHeaderTextStyle())

    def tabSettingsRootPath(self):
        """ label, textbox and folder selection for root folder  """
        label = QLabel(self.settingsContainer)
        label.setGeometry(8, 32, 100, 24)
        label.setText('Root Path:')
        label.setStyleSheet('color: #2A3241, background-color: rgba(0, 0, 0, 0%)')

        self.settingsRootFolder = QLineEdit(self.settingsContainer)
        self.settingsRootFolder.setGeometry(
            85,
            32,
            self.settingsContainer.width() - 93,
            24,
        )
        self.settingsRootFolder.setStyleSheet(windowStyle.tabSettingsRootPathEditStyle())
        self.settingsRootFolder.setPlaceholderText('enter ArcDPS logging path')
        self.settingsRootFolder.setReadOnly(True)

        changeButton = QPushButton(self.settingsRootFolder)
        changeButton.setGeometry(self.settingsRootFolder.width() - 22, 2, 20, 20)
        changeButton.setIcon(QIcon('resources/graphics/icons/explorer_48x48.png'))
        changeButton.setIconSize(QSize(14, 14))
        changeButton.setToolTip('Select Folder')
        changeButton.clicked.connect(self.tabSettingsRootPathButtonAction)

    def tabSettingsPollingRate(self):
        """ polling rate selection """
        label = QLabel(self.settingsContainer)
        label.setGeometry(8, 60, 100, 24)
        label.setText('Polling Rate:')
        label.setStyleSheet('color: #2A3241, background-color: rgba(0, 0, 0, 0%)')

        self.pollingRate = QSpinBox(self.settingsContainer)
        self.pollingRate.setGeometry(85, 60, 40, 24)
        self.pollingRate.setMaximum(10)
        self.pollingRate.setMinimum(1)
        self.pollingRate.lineEdit().setReadOnly(True)
        self.pollingRate.setStyleSheet(windowStyle.tabSettingsPollingRateBoxStyle())

    def tabSettingsHeaderReport(self):
        """ log settings label """
        header = QLabel(self.settingsContainer)
        header.setGeometry(8, 92, 200, 24)
        header.setText('Report Settings')
        header.setStyleSheet(windowStyle.tabDiscordHeaderTextStyle())

    def tabSettingsUserToken(self):
        """ label and textbox to edit userToken """
        label = QLabel(self.settingsContainer)
        label.setGeometry(8, 120, 100, 24)
        label.setText('UserToken:')
        label.setStyleSheet('color: #2A3241, background-color: rgba(0, 0, 0, 0%)')

        self.userToken = QLineEdit(self.settingsContainer)
        self.userToken.setGeometry(85, 120, self.settingsContainer.width() - 93, 24)
        self.userToken.setEchoMode(QLineEdit.EchoMode.Password)
        self.userToken.setStyleSheet(windowStyle.tabSettingsUserTokenEditStyle())

        self.userTokenShowButton = QPushButton(self.settingsContainer)
        self.userTokenShowButton.setGeometry(
            self.userToken.x() + self.userToken.width() - 22,
            self.userToken.y() + 2,
            20,
            20
        )
        self.userTokenShowButton.setIcon(QIcon('resources/graphics/icons/show_48x48.png'))
        self.userTokenShowButton.setIconSize(QSize(14, 14))
        self.userTokenShowButton.setToolTip('Show/Hide UserToken')
        self.userTokenShowButton.setStyleSheet(windowStyle.tabSettingsUserTokenShowButtonStyle())
        self.userTokenShowButton.clicked.connect(self.tabSettingsShowUserTokenButtonAction)

    def tabSettingsAnonymousCheckBox(self):
        """ checkbox for anonymous logs """
        label = QLabel(self.settingsContainer)
        label.setGeometry(8, 148, 150, 24)
        label.setText('Anonymous Reports: ')
        label.setStyleSheet('color: #2A3241, background-color: rgba(0, 0, 0, 0%)')
        self.anonymousCheck = QCheckBox(self.settingsContainer)
        self.anonymousCheck.setGeometry(128, 149, 24, 24)

    def tabSettingsApplyButton(self):
        """ create apply settings button for settings tab """
        self.tabSettingsApplyBtn = QPushButton(self.settingsContainer)
        self.tabSettingsApplyBtn.setGeometry(
            self.settingsContainer.width() - 75,
            self.settingsContainer.height() - 32,
            67,
            24,
        )
        self.tabSettingsApplyBtn.setStyleSheet(windowStyle.tabSettingsWhiteButtonStyle())
        self.tabSettingsApplyBtn.setText('Apply')
        self.tabSettingsApplyBtn.clicked.connect(self.tabSettingsApplyButtonAction)

    def tabSettingsCancelButton(self):
        """ create cancel settings button for settings tab """
        self.tabSettingsCancelBtn = QPushButton(self.settingsContainer)
        self.tabSettingsCancelBtn.setGeometry(
            self.tabSettingsApplyBtn.x() - 75,
            self.settingsContainer.height() - 32,
            67,
            24,
        )
        self.tabSettingsCancelBtn.setStyleSheet(windowStyle.tabSettingsWhiteButtonStyle())
        self.tabSettingsCancelBtn.setText('Cancel')
        self.tabSettingsCancelBtn.clicked.connect(self.tabSettingsCancelButtonAction)

    def tabSettingsOkButton(self):
        """ create ok settings button for settings tab """
        button = QPushButton(self.settingsContainer)
        button.setGeometry(
            self.tabSettingsCancelBtn.x() - 75,
            self.settingsContainer.height() - 32,
            67,
            24,
        )
        button.setStyleSheet(windowStyle.tabSettingsGreenButtonStyle())
        button.setText('OK')
        button.clicked.connect(self.tabSettingsOkButtonAction)

    # # # THREAD INIT
    def initThread(self):
        self.fileServiceThread()

    def fileServiceThread(self):
        """ Thread: looking for new files in root folder """
        self.fileThread = FileServiceThread(self.configObject)
        self.fileThread.signal.newData.connect(self.fileServiceThreadAction)
        self.fileThread.start()

    def uploadThread(self, bossObject: BossObject):
        """ Thread: uploads new log for basic information, updates bossList """
        uploadThread = UploadServiceThread(data=bossObject, config=self.configObject)
        uploadThread.signal.finishedObject.connect(self.discordUploadCheck)
        self.threadPool.start(uploadThread)

    def discordThread(self, url: str):
        """ Thread: request detailed log information, parse them and post on discord via webhook """
        if -1 < self.configObject.selectedServer < len(self.configObject.serverList):
            discordThread = DiscordServiceThread(url=url, configObject=self.configObject)
            self.threadPool.start(discordThread)

    def saveConfigThread(self):
        """ Thread: writes current configObject to files """
        saveConfigThread = SaveConfigThread(self.configObject)
        self.threadPool.start(saveConfigThread)

    # # # BUTTON ACTIONS
    # title bar
    def titleBarCloseButtonAction(self):
        """ stops all running threads and shutting down app """
        self.threadPool.clear()
        # TODO: add thread stops for file thread
        print('Exit successful!', flush=True)
        sys_exit()

    def titleBarMinimizeButtonAction(self):
        """ Simulates press on minimize button """
        self.showMinimized()

    # side bar
    def sideBarHomeButtonAction(self):
        """ Changes active tab """
        self.setActiveTab(0)

    def sideBarDiscordButtonAction(self):
        """ Changes active tab """
        self.setActiveTab(1)
        self.updateDiscordBossList()
        self.updateDiscordDisplayName()
        self.updateDiscordServerList()

    def sideBarSettingsButtonAction(self):
        """ Changes active tab """
        self.setActiveTab(2)
        self.updateSettingsRootPath()
        self.updateSettingsPollingRate()
        self.updateSettingsUserToken()
        self.updateSettingsAnonymousLog()

        self.userToken.setEchoMode(QLineEdit.EchoMode.Password)
        self.userTokenShowButton.setIcon(QIcon('resources/graphics/icons/show_48x48.png'))

    def sideBarGitHubButtonAction(self):
        """ opens github url """
        url = 'https://github.com/Jatzelberger'
        self.openURLinBrowser(url)

    # home tab
    def bossListContextMenuCopyURLAction(self):
        """ get log url and saves it to clipboard """
        url = self.bossList.itemWidget(self.bossList.currentItem()).getBossObject().url
        self.stringToClipBoard(url)

    def bossListContextMenuOpenBrowserAction(self):
        """ get log url and opens it in a new browser tab"""
        url = self.bossList.itemWidget(self.bossList.currentItem()).getBossObject().url
        self.openURLinBrowser(url)

    def bossListContextMenuOpenExplorerAction(self):
        """ opens file explorer on log folder """
        path = self.bossList.itemWidget(self.bossList.currentItem()).getBossObject().path
        self.openFileInExplorer(path)

    def tabHomeTextBoxDeleteButtonAction(self):
        """ clears text box for custom discord posts by setting text to empty string """
        self.homeURLTextBox.setText('')

    def tabHomeDiscordPostButtonAction(self):
        """ posts log on discord, checks if log is uploaded first """
        if self.homeURLTextBox.text() != '':
            self.discordThread(self.homeURLTextBox.text())
            self.homeURLTextBox.setText('')
        else:
            item = self.bossList.currentItem()
            if item is not None:
                data = self.bossList.itemWidget(item).getBossObject()
                if data.success is not None and data.url != '':
                    self.discordThread(data.url)

    def tabHomeStartWebhookButtonAction(self):
        """ switches between enabled and disabled automatic discord posting """
        if self.startWebhookButton.text() == 'START':
            self.startWebhookButton.setText('STOP')
            self.startWebhookButton.setIcon(QIcon('resources/graphics/icons/stop_48x48.png'))
            self.startWebhookButton.setToolTip('stop automatic discord posting')
            self.automaticPosting = True
        else:
            self.startWebhookButton.setText('START')
            self.startWebhookButton.setIcon(QIcon('resources/graphics/icons/start_48x48.png'))
            self.startWebhookButton.setToolTip('start automatic discord posting')
            self.automaticPosting = False

    def tabDiscordServerListAddButtonAction(self):
        """ opens popup to add new webhook to server list """
        if self.serverListAddPopup.isHidden():
            self.serverListAddPopup.show()
        else:
            self.serverListAddPopup.hide()

    def tabDiscordServerListAddAction(self):
        """ Adds new webhook to server list"""
        if self.serverListNameEdit.text() != '' and self.serverListURLEdit.text() != '':
            self.addNewServer(name=self.serverListNameEdit.text(), url=self.serverListURLEdit.text())

    def tabDiscordServerListRemoveButtonAction(self):
        """ removes selected webhook from server list """
        index = self.serverList.currentIndex()
        self.serverList.removeItem(index)
        self.serverList.setCurrentIndex(-1)
        self.configObject.serverList.pop(index)
        self.configObject.selectedServer = -1

    def tabDiscordOkButtonAction(self):
        """ saves all settings and return to home screen"""
        self.saveDiscordSettings()
        self.setActiveTab(0)

    def tabDiscordApplyButtonAction(self):
        """ saves all settings and stays on discord tab"""
        self.saveDiscordSettings()

    def tabDiscordCancelButtonAction(self):
        """ dismiss all changes and return back to home tab"""
        self.setActiveTab(0)

    def tabSettingsRootPathButtonAction(self):
        """ opens root path selection explorer """
        file = QFileDialog.getExistingDirectory(self, caption='Select Folder', directory=self.settingsRootFolder.text())
        if file == '':
            self.settingsRootFolder.setText(self.configObject.rootPath)
        else:
            self.settingsRootFolder.setText(file + '/')

    def tabSettingsShowUserTokenButtonAction(self):
        """ Shows/Hides UserToken from LinEdit """
        if self.userToken.echoMode() == QLineEdit.EchoMode.Password:
            self.userToken.setEchoMode(QLineEdit.EchoMode.Normal)
            self.userTokenShowButton.setIcon(QIcon('resources/graphics/icons/hide_48x48.png'))
        else:
            self.userToken.setEchoMode(QLineEdit.EchoMode.Password)
            self.userTokenShowButton.setIcon(QIcon('resources/graphics/icons/show_48x48.png'))

    def tabSettingsOkButtonAction(self):
        """ saves all settings and return to home screen"""
        self.saveSettingsSettings()
        self.setActiveTab(0)

    def tabSettingsApplyButtonAction(self):
        """ saves all settings and stays on discord tab"""
        self.saveSettingsSettings()

    def tabSettingsCancelButtonAction(self):
        """ dismiss all changes and return back to home tab"""
        self.setActiveTab(0)

    # # # THREAD CONNECT ACTIONS
    def fileServiceThreadAction(self, value: BossObject):
        """ FileServiceThread: adds new log item when available """
        self.newBossListItem(value)

    # # # BACKEND FUNCTIONS
    def setActiveTab(self, tabID: int):
        """ switches between tabs """
        button = [self.sideBarHomeBtn, self.sideBarDiscordBtn, self.sideBarSettingsBtn]
        container = [self.homeContainer, self.discordContainer, self.settingsContainer]
        for tab in range(0, len(button)):
            if tab == tabID:
                button[tab].setStyleSheet(windowStyle.sideBarButtonActiveStyle())
                container[tab].show()
            else:
                button[tab].setStyleSheet(windowStyle.sideBarButtonInactiveStyle())
                container[tab].hide()

    def newBossListItem(self, bossObject: BossObject, old: bool = False):
        """ Adds new boss item to bossList """
        newBossWidget = BossListEntryWidget()

        newListItem = QListWidgetItem()
        newListItem.setSizeHint(QSize(350, 50))

        self.bossList.insertItem(0, newListItem)
        self.bossList.setItemWidget(newListItem, newBossWidget)

        bossObject.widgetID = newBossWidget
        newBossWidget.updateData(bossObject)

        if not old:
            self.uploadThread(bossObject)  # do not upload if old flag is set

    def eventFilter(self, source, event):
        """ Event filter to open context menu on item in boss list """
        # open context menu when right click on item
        if event.type() == QEvent.Type.ContextMenu \
                and source is self.bossList \
                and source.itemAt(event.pos()) is not None:
            self.tabHomeBossListContextMenu(source, event)
            return True
        # clear selections when right click next to an item in boss list
        if event.type() == QEvent.Type.ContextMenu \
                and source is self.bossList \
                and source.itemAt(event.pos()) is None:
            self.bossList.clearSelection()
            return True
        # return default event
        return super().eventFilter(source, event)

    def discordUploadCheck(self, value: BossObject):
        """ For automatic uploading: uploads boss object if it has required flags """
        if value.webhook and value.success and self.automaticPosting:
            self.discordThread(value.url)

    def stringToClipBoard(self, text: str):
        """ copy given string to clipboard """
        cmd = 'echo | set /p nul=' + text.strip() + '| clip'
        os_system(cmd)

    def openURLinBrowser(self, url: str):
        """ open url in new browser tab """
        web_open(url, new=2)  # 2: new tab

    def openFileInExplorer(self, path: str):
        """ open path in explorer """
        file_name = path.split('/')[-1]
        path = path.replace(file_name, '')
        path = path.replace('/', '\\')
        sub_Popen(f'explorer "{path}"')

    def updateDiscordBossList(self):
        """ updates enabledBossList from configObject"""
        self.enabledBossesList.clear()
        for bossID in self.configObject.boss:
            newListItem = QListWidgetItem(self.configObject.boss[bossID]['name'])
            newListItem.setSizeHint(QSize(190, 25))
            newListItem.setFlags(newListItem.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            if self.configObject.boss[bossID]['post']:
                newListItem.setCheckState(Qt.CheckState.Checked)
            else:
                newListItem.setCheckState(Qt.CheckState.Unchecked)
            self.enabledBossesList.addItem(newListItem)

    def updateDiscordDisplayName(self):
        """ updates webhook display name """
        self.webhookDisplayName.setText(self.configObject.displayName)

    def updateDiscordServerList(self):
        """ updates webhook server list """
        self.serverList.clear()
        for server in self.configObject.serverList:
            self.serverList.addItem(server[0])
        self.serverList.setCurrentIndex(self.configObject.selectedServer)

    def saveDiscordSettings(self):
        """ saves discord settings to configObject and to file"""
        enabledBosses = []
        for i in range(0, self.enabledBossesList.count()):
            state = self.enabledBossesList.item(i).checkState() == Qt.CheckState.Checked
            for bossID in self.configObject.boss:
                if self.configObject.boss[bossID]['name'] == self.enabledBossesList.item(i).text():
                    self.configObject.boss[bossID]['post'] = state
                    enabledBosses.append((bossID, state))
        self.configObject.displayName = self.webhookDisplayName.text()
        self.configObject.selectedServer = self.serverList.currentIndex()
        self.saveConfigThread()

    def addNewServer(self, name: str, url: str):
        """ Adds new item to serverList"""
        self.configObject.serverList.append([name, url])
        self.serverListNameEdit.setText('')
        self.serverListURLEdit.setText('')
        self.serverList.addItem(name)
        self.serverListAddPopup.hide()

    def updateSettingsRootPath(self):
        """ updates root path """
        self.settingsRootFolder.setText(self.configObject.rootPath)

    def updateSettingsPollingRate(self):
        """ updates polling rate """
        self.pollingRate.setValue(self.configObject.pollingRate)

    def updateSettingsUserToken(self):
        """ updates userToken"""
        self.userToken.setText(self.configObject.userToken)

    def updateSettingsAnonymousLog(self):
        """ updates anonymousLog selection """
        self.anonymousCheck.setChecked(self.configObject.anonymousLog)

    def saveSettingsSettings(self):
        """ save settings to configObject and starts saveConfigThread """
        if self.settingsRootFolder.text() != '':
            self.configObject.rootPath = self.settingsRootFolder.text()
        self.configObject.pollingRate = self.pollingRate.value()
        if self.userToken.text() != '':
            self.configObject.userToken = self.userToken.text()
        self.configObject.anonymousLog = self.anonymousCheck.isChecked()
        self.saveConfigThread()
