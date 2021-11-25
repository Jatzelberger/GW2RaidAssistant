from zipfile import ZipFile
from collections import namedtuple
from struct import unpack

import os


Header = namedtuple('Header', 'magic version evtc_version boss_id')
Agent = namedtuple('Agent', 'address profession elite_mask toughness '
                            'concentration healing_power hitbox_width '
                            'condition_damage hitbox_height name')


def _read_uint32(stream):
    """Unpack a uint32 from a stream."""
    return unpack('<I', stream.read(4))[0]


def _read_header(stream):
    """Unpack a header from a stream."""
    data = stream.read(16)
    return Header._make(unpack('<I8schx', data))


def _read_agent(stream):
    """Unpack an agent from a stream."""
    data = stream.read(96)
    return Agent._make(unpack('<QIIhhhhhh68s', data))


def parse_evtc(stream):
    """Parse an evtc file and return the combat events in a meaningful format."""
    header = _read_header(stream)

    agent_count = _read_uint32(stream)
    agents_by_address = {}
    for _ in range(agent_count):
        agent = _read_agent(stream)
        agents_by_address[agent.address] = agent

    return header, agents_by_address


class EvctService:
    def __init__(self, file: str):
        self.file = file

        self.header = None
        self.agents_by_address = None

    def __checkZevtc(self) -> bool:
        return self.file.split('.')[-1] == 'zevtc'

    def __unpackZevtc(self):
        if not os.path.exists('resources/backend/tempFiles/'):
            os.mkdir('resources/backend/tempFiles/')
        with ZipFile(self.file) as zip_data:
            file_name = zip_data.namelist()[0]
            zip_data.extractall('resources/backend/tempFiles/')
        self.file = 'resources/backend/tempFiles/' + file_name

    def __clearFile(self):
        os.remove(self.file)

    def readFile(self):
        if self.__checkZevtc():
            self.__unpackZevtc()
        with open(self.file, 'rb') as byte_data:
            self.header, self.agents_by_address = parse_evtc(byte_data)
        self.__clearFile()

    def getBossID(self) -> int:
        return self.header.boss_id

    def getPlayer(self) -> dict:
        """Returns dictionary with char_names, account_names and subgroups"""
        player_dict = {}
        for names in self.agents_by_address:
            player = self.agents_by_address[names].name.replace(b'\x00', b'').decode('utf-8')
            if ':' in player and '.' in player:
                player_names = player[0:len(player) - 1].split(':')
                character_name = player_names[0]
                account_name = player_names[1]
                group = player[-1]
                player_dict[character_name] = {'account_name': account_name, 'subgroup': group}
        return player_dict
