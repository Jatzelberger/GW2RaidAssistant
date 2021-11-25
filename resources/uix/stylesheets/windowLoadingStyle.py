def windowContainerStyle():
    return """
        QLabel {
            background-color: #FEF5ED;
        }
    """


def titleImageWidgetStyle():
    return """
        QLabel {
            background-color: rgba(0, 0, 0, 0%);
        }
    """


def titleTextWidgetStyle():
    return """
        QLabel {
            background-color: rgba(0, 0, 0, 0%);
            font-size: 40px;
            font-weight: bold;
            color: #383E56
        }
    """


def authorTextWidgetStyle():
    return """
        QLabel {
            background-color: rgba(0, 0, 0, 0%);
            font-size: 17px;
            color: #383E56
        }
    """


def progressBarWidgetStyle():
    return """
        QProgressBar {
            border-radius: 0px;
            border: 0px;
            background-color: rgba(0, 0, 0, 0%);
        }
        QProgressBar::chunk {
            background-color: #99A799;
            border-radius: 0px;
            border: 0px
        }
    """

