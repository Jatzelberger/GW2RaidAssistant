from PyQt6.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot
from resources.backend.configObject import ConfigObject
import resources.backend.services.configService as configService
from time import sleep


class ConfigThreadSignal(QObject):
    newLogStorage = pyqtSignal(dict, name="NEW_LOGS")  # Emits signal with list of stores logs
    newProgress = pyqtSignal(int, name="NEW_PROGRESS")  # Emits signal of new progressBar value
    newEndSignal = pyqtSignal(bool, name="END_SIGNAL")  # Emits signal on thread ending (true: success, false: error)


class ConfigThread(QRunnable):
    def __init__(self, config: ConfigObject):
        super(ConfigThread, self).__init__()

        self.signal = ConfigThreadSignal()

        self.config = config  # writes directly on config object -> need no return

        self.basicConfigPath = 'resources/config/basicConfig.ini'
        self.bossConfigPath = 'resources/config/bossConfig.ini'
        self.discordConfigPath = 'resources/config/discordConfig.ini'
        self.bossStoragePath = 'resources/config/bossStorage.ini'

    @pyqtSlot()
    def run(self):
        try:
            self.signal.newProgress.emit(10)

            # check basicConfig.ini
            if not configService.configExists(self.basicConfigPath):
                configService.newBasicConfig(self.basicConfigPath)
            self.signal.newProgress.emit(20)

            # check bossConfig.ini
            if not configService.configExists(self.bossConfigPath):
                configService.newBossConfig(self.bossConfigPath)
            self.signal.newProgress.emit(30)

            # check discordConfig.ini
            if not configService.configExists(self.discordConfigPath):
                configService.newDiscordConfig(self.discordConfigPath)
            self.signal.newProgress.emit(40)

            # read files
            basicConfig = configService.parseConfigFile(self.basicConfigPath)
            self.signal.newProgress.emit(60)
            bossConfig = configService.parseConfigFile(self.bossConfigPath)
            self.signal.newProgress.emit(70)
            discordConfig = configService.parseConfigFile(self.discordConfigPath)
            self.signal.newProgress.emit(80)

            # store data in configObject
            configService.storeConfigObject(self.config, basicConfig, bossConfig, discordConfig)

            # check bossStorage
            if not configService.configExists(self.bossStoragePath):
                configService.newBossStorage(self.bossStoragePath)
                self.signal.newLogStorage.emit({})
            else:
                self.signal.newLogStorage.emit(configService.parseConfigFile(self.bossStoragePath))
            self.signal.newProgress.emit(90)

            sleep(0.5)
            self.signal.newProgress.emit(100)
            sleep(0.5)
            self.signal.newEndSignal.emit(True)

        except Exception as e:
            # Handle exception in case something went wrong or some data is corrupted
            # Deleting all config files and restarting should solve the problem!
            print(e)
            self.signal.newProgress.emit(100)
            sleep(3)
            self.signal.newEndSignal.emit(False)
