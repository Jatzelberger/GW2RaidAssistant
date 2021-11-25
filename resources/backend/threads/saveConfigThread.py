from PyQt6.QtCore import QRunnable, pyqtSlot
from resources.backend.configObject import ConfigObject
import resources.backend.services.configService as configService


class SaveConfigThread(QRunnable):
    def __init__(self, config: ConfigObject):
        super(SaveConfigThread, self).__init__()

        self.config = config  # writes directly on config object -> need no return

        self.basicConfigPath = 'resources/config/basicConfig.ini'
        self.bossConfigPath = 'resources/config/bossConfig.ini'
        self.discordConfigPath = 'resources/config/discordConfig.ini'

    @pyqtSlot()
    def run(self):
        try:
            configService.saveNewConfig(
                config=self.config,
                basicPath=self.basicConfigPath,
                bossPath=self.bossConfigPath,
                discordPath=self.discordConfigPath
            )
        except Exception as e:
            print(e)