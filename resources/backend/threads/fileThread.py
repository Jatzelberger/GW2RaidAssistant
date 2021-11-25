import os

from PyQt6.QtCore import QObject, pyqtSignal, QThread
from time import sleep
from datetime import datetime
from resources.backend.configObject import ConfigObject
from resources.backend.bossObject import BossObject
from resources.backend.services.fileService import FileService
from resources.backend.services.evtcService import EvctService


class FileServiceThreadSignal(QObject):
    newData = pyqtSignal(BossObject)


class FileServiceThread(QThread):
    def __init__(self, config: ConfigObject):
        QThread.__init__(self, parent=None)
        self.signal = FileServiceThreadSignal()
        self.config = config

    def run(self):
        fileService = FileService()
        fileService.setup(
            folder=self.config.rootPath,
            file_name='*',
            file_extension='*evtc',
        )

        oldFile = fileService.get()
        while True:
            newFile = fileService.get()
            if newFile != oldFile:
                oldFile = newFile
                try:  # could be corrupted file
                    evtcService = EvctService(newFile)
                    evtcService.readFile()
                    newBossObject = BossObject(
                        id=evtcService.getBossID(),
                        time=datetime.fromtimestamp(os.path.getmtime(newFile)),
                        path=newFile,
                    )
                    for bossID in self.config.boss:
                        if str(newBossObject.id) in str(bossID):
                            newBossObject.name = self.config.boss[bossID]['name']
                            newBossObject.icon = self.config.boss[bossID]['icon']
                            newBossObject.webhook = self.config.boss[bossID]['post']

                    self.signal.newData.emit(newBossObject)
                except Exception:
                    pass  # Ignore file, maybe corrupted
            sleep(self.config.pollingRate)


