from PyQt6.QtCore import QRunnable, pyqtSlot
from resources.backend.services.discordService import DiscordService
from resources.backend.services.networkService import WebhookDataService
from resources.backend.configObject import ConfigObject


class DiscordServiceThread(QRunnable):
    def __init__(self, url: str, configObject: ConfigObject):
        super(DiscordServiceThread, self).__init__()
        self.url = url
        self.config = configObject

    @pyqtSlot()
    def run(self):
        try:
            webhookDataService = WebhookDataService(self.url)
            data = webhookDataService.getStrippedData()
        except Exception as e:
            print(e)
            return

        try:
            discordService = DiscordService(data=data, url=self.url, config=self.config)
            discordService.sendWebhook()
        except Exception as e:
            print(e)
            return
