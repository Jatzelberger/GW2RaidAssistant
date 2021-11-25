from dataclasses import dataclass, field


@dataclass
class ConfigObject:
    rootPath: str = ''  # root path for fileWatcher
    pollingRate: int = 0  # polling rate for fileWatcher
    storageCount: int = 0  # amount of stored logs

    userToken: str = ''  # unique user token for dps.report
    anonymousLog: bool = False  # activate anonymous logs
    displayName: str = ''  # name shown in discord postings, emtpy string for character name

    selectedServer: int = -1  # stores selected server (index of serverList)
    serverList: list = field(default_factory=list)  # server list containing tuple with server name and url

    emojis: dict = field(default_factory=dict)  # see emoji doc for reference
    boss: dict = field(default_factory=dict)  # stores boss information by bossID
