from PyQt6.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot
from resources.backend.services.networkService import ReportService
from resources.backend.bossObject import BossObject
from resources.backend.configObject import ConfigObject


class UploadServiceSignal(QObject):
    finishedObject = pyqtSignal(BossObject, name="OBJECT")


class UploadServiceThread(QRunnable):
    def __init__(self, data: BossObject, config: ConfigObject):
        super(UploadServiceThread, self).__init__()
        self.signal = UploadServiceSignal()
        self.data = data
        self.config = config

    @pyqtSlot()
    def run(self):
        reportService = ReportService(
            targetURL='https://dps.report/uploadContent',
            userToken=self.config.userToken,
            anonymous=self.config.anonymousLog,
        )
        status, value = reportService.uploadFile(self.data.path)
        if status == 'error':
            code = str(value['code'])
            widget = self.data.widgetID
            widget.setError(str(code))
        else:
            self.data.success = value['encounter']['success']
            self.data.cm = value['encounter']['isCm']
            if self.data.name == 'Loading...':
                self.data.name = value['encounter']['boss']
            self.data.url = value['permalink']
            widgetID = self.data.widgetID
            widgetID.updateData(self.data)
            self.signal.finishedObject.emit(self.data)
