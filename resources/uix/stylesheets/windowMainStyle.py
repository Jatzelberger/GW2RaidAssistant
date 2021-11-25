# MAIN WINDOW OBJECTS
def windowContainerStyle():
    return """
        QLabel {
            background-color: #FEF5ED;
        }
    """


def titleBarBackgroundStyle():
    return """
        QLabel {
            background-color: #99A799;
            font-weight: bold;
            color: #2A3241;
            font-size: 14px;
        }
    """


def titleBarCloseButtonStyle():
    return """
        QPushButton {
            background-color: #99A799;
            border-radius: 10px;
            border: 0px;
        }
        QPushButton:hover:!pressed {
            background-color: rgba(0, 0, 0, 15%);
        }
        QPushButton:hover:pressed {
            background-color: rgba(0, 0, 0, 22%);
        }
    """


def titleBarMinimizeButtonStyle():
    return """
        QPushButton {
            background-color: #99A799;
            border-radius: 10px;
            border: 0px;
        }
        QPushButton:hover:!pressed {
            background-color: rgba(0, 0, 0, 15%);
        }
        QPushButton:hover:pressed {
            background-color: rgba(0, 0, 0, 22%);
        }
    """


# SIDE BAR
def sideBarBackgroundStyle():
    return """
        QLabel {
            background-color: #D3E4CD;
        }
    """


def sideBarButtonInactiveStyle():
    return """
        QPushButton {
            background-color: #D3E4CD;
            border: 0px;
        }
    """


def sideBarButtonActiveStyle():
    return """
        QPushButton {
            background-color: #FEF5ED;
            border: 0px;
        }
    """


def sideBarGithubButtonStyle():
    return """
        QPushButton {
            background-color: #D3E4CD;
            border-radius: 12px;
            border: 0px;
        }
        QPushButton:hover:!pressed {
            background-color: rgba(0, 0, 0, 15%);
        }
        QPushButton:hover:pressed {
            background-color: rgba(0, 0, 0, 22%);
        }
    """


def tabContainerBackgroundStyle():
    return """
        QLabel {
            background-color: rgba(0, 0, 0, 0%);
        }
    """


# HOME TAB
def bossListStyle():
    return """
        QListWidget {
            background-color: #FEF5ED;
            border: 1px solid #D3E4CD;
        }
        QListWidget::item:hover {
            background-color: #D3E4CD;
        }
        QListWidget::item:selected {
            background-color: #ADC2A9;
            border: 0px
        }
    """


def customScrollBarStyle():
    return """
        QScrollBar {
            width: 5px;
            background-color: rgba(0, 0, 0, 0%);
            border-left: 1px solid #FEF5ED
        }
        QScrollBar::sub-page:vertical {
            background-color: #D3E4CD;
            width: 5px;
        }
        QScrollBar::add-page:vertical {
            background-color: #D3E4CD;
            width: 5px;
        }
        QScrollBar::handle:vertical {
            border: 0px solid black;
            background: #ADC2A9;
            border-radius: 0px;
        }
        QScrollBar::add-line:vertical {
            width: 0px;
            height: 0px;
        }
        QScrollBar::sub-line:vertical {
            width: 0px;
            height: 0px;
        }
    """


def bossListContextMenuStyle():
    return """
        QMenu {
            background-color: #FEF5ED;
            color: #2A3241;
            border: 1px solid #ADC2A9;
            padding: 2px 2px 2px 2px;
        }
        QMenu::item {
            padding: 2px 0px 2px 0px;
        }
        QMenu::item:selected {
            background-color: #D3E4CD;
            color: #2A3241;
        }
        QMenu::item:hover {
            background-color: #D3E4CD;
        }
    """


def tabHomeStartWebhookButtonStyle():
    return """
        QPushButton {
            text-align: left;
            background-color: #D3E4CD;
            color: #2A3241;
            font-weight: bold;
            border: 1px solid #ADC2A9;
        }
        QPushButton:hover:!pressed {
            background-color: #ADC2A9;
        }
        QPushButton:hover:pressed {
            background-color: #99A799;
        }
    """


def tabHomeURLTextBoxStyle():
    return """
        QLineEdit {
            background-color: #FFFAF5;
            border: 1px solid #ADC2A9;
            padding-left: 2px;
            padding-right: 22px;
        }
    """


def tabHomeDiscordPostButtonStyle():
    return """
        QPushButton {
            text-align: center;
            background-color: #D3E4CD;
            color: #2A3241;
            font-weight: bold;
            border: 1px solid #ADC2A9;
        }
        QPushButton:hover:!pressed {
            background-color: #ADC2A9;
        }
        QPushButton:hover:pressed {
            background-color: #99A799;
        }
    """


def tabHomeURLTextBoxDeleteButtonStyle():
    return """
        QPushButton {
            background-color: rgba(0, 0, 0, 0%);
        }
    """


# DISCORD TAB
def tabDiscordEnabledBossesListStyle():
    return """
        QListWidget {
            background-color: #FEF5ED;
            border: 1px solid #D3E4CD;
        }
        QListWidget::item:hover {
            background-color: #FEF5ED;
        }
        QListWidget::item:selected {
            background-color: #FEF5ED;
            border: 0px;
        }
    """


def tabDiscordServerTable():
    return """
        QComboBox {
            background-color: #FFFAF5;
            border: 1px solid #D3E4CD;
            color: black;
            padding-left: 5px;
        }
        QComboBox::drop-down {
            border: 0px solid black;
            background: url(resources/graphics/icons/dropdown_20x20.png);
            width: 20px;
            height: 20px;
        }
        QComboBox::drop-down {
            border: solid; 
            width: 20px;
        }
        QComboBox QAbstractItemView {
            background-color: #FEF5ED;
            border: 1px solid #D3E4CD;
            color: black;
        }
        QComboBox QAbstractItemView::item:hover {
            background-color: #D3E4CD;
            color: black;
        }
        QComboBox QAbstractItemView::item:selected {
            background-color: #D3E4CD;
            color: black;
        }
    """


def tabDiscordGreenButtonStyle():
    return """
        QPushButton {
            text-align: center;
            background-color: #D3E4CD;
            color: #2A3241;
            font-weight: bold;
            border: 1px solid #ADC2A9;
        }
        QPushButton:hover:!pressed {
            background-color: #ADC2A9;
        }
        QPushButton:hover:pressed {
            background-color: #99A799;
        }
    """


def tabDiscordWhiteButtonStyle():
    return """
        QPushButton {
            text-align: center;
            background-color: #FEF5ED;
            color: #2A3241;
            font-weight: bold;
            border: 1px solid #ADC2A9;
        }
        QPushButton:hover:!pressed {
            background-color: #D3E4CD;
        }
        QPushButton:hover:pressed {
            background-color: #ADC2A9;
        }
    """


def tabDiscordDisplayNameEditStyle():
    return """
    QLineEdit {
            background-color: #FFFAF5;
            border: 1px solid #ADC2A9;
            padding-left: 2px;
        }
    """


def tabDiscordHeaderTextStyle():
    return """
        QLabel {
            background-color: rgba(0, 0, 0, 0%);
            color: #2A3241;
            font-size: 13px;
            font-weight: bold;
        }
    """


def tabDiscordServerListPopupStyle():
    return """
        QLabel {
            background-color: #FEF5ED;
            border: 1px solid #D3E4CD;
        }
        QLineEdit {
            background-color: #FFFAF5;
            border: 1px solid #ADC2A9;
            padding-left: 2px;
        }
    """


# SETTINGS TAB
def tabSettingsGreenButtonStyle():
    return """
        QPushButton {
            text-align: center;
            background-color: #D3E4CD;
            color: #2A3241;
            font-weight: bold;
            border: 1px solid #ADC2A9;
        }
        QPushButton:hover:!pressed {
            background-color: #ADC2A9;
        }
        QPushButton:hover:pressed {
            background-color: #99A799;
        }
    """


def tabSettingsWhiteButtonStyle():
    return """
        QPushButton {
            text-align: center;
            background-color: #FEF5ED;
            color: #2A3241;
            font-weight: bold;
            border: 1px solid #ADC2A9;
        }
        QPushButton:hover:!pressed {
            background-color: #D3E4CD;
        }
        QPushButton:hover:pressed {
            background-color: #ADC2A9;
        }
    """


def tabSettingsRootPathEditStyle():
    return """
        QLineEdit {
            background-color: #FFFAF5;
            border: 1px solid #ADC2A9;
            padding-left: 2px;
            padding-right: 22px;
        }
        QPushButton {
            background-color: rgba(0, 0, 0, 0%);
            border: 0px solid black;
        }
    """


def tabSettingsPollingRateBoxStyle():
    return """
        QSpinBox {
            background-color: #FFFAF5;
            selection-background-color: #FFFAF5;
            selection-color: black;
            border: 1px solid #ADC2A9;
            padding-left: 2px;
        }
        QSpinBox:selected {
            background-color: white;
        }
                
    """


def tabSettingsUserTokenEditStyle():
    return """
        QLineEdit {
            background-color: #FFFAF5;
            border: 1px solid #ADC2A9;
            padding-left: 2px;
            padding-right: 22px;
        }
    """


def tabSettingsUserTokenShowButtonStyle():
    return """
        QPushButton {
            background-color: rgba(0, 0, 0, 0%);
            border: 0px solid black;
        }
    """