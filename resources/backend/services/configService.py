import os
from configparser import ConfigParser
from resources.backend.configObject import ConfigObject
from resources.backend.services.networkService import newUserToken


def configExists(path: str) -> bool:
    """ Check if file on given path exists """
    return os.path.exists(path)


def newBasicConfig(path: str):
    """ Creates default basicConfig.ini """
    defaultRootPath = f'C:/Users/{os.getlogin()}/Documents/Guild Wars 2/addons/arcdps/arcdps.cbtlogs/'
    file = ConfigParser()

    userTokenTuple = newUserToken()
    if userTokenTuple[0] == 'error':
        print(userTokenTuple[1])
        userToken = ''
    else:
        userToken = userTokenTuple[1]

    file.add_section('explorer')
    file.set('explorer', 'rootPath', defaultRootPath)
    file.set('explorer', 'pollingRate', '2')

    file.add_section('storage')
    file.set('storage', 'count', '20')

    file.add_section('log')
    file.set('log', 'userToken', userToken)
    file.set('log', 'anonymous', 'false')

    with open(path, 'w') as file_stream:
        file.write(file_stream)


def newBossConfig(path: str):
    """ Creates default bossConfig.ini """
    file = ConfigParser()

    # WING 1
    file.add_section('15438')
    file.set('15438', 'post', 'true')
    file.set('15438', 'name', 'Vale Guardian')
    file.set('15438', 'icon', 'resources/graphics/bosses/vale_guardian.png')

    file.add_section('15429')
    file.set('15429', 'post', 'true')
    file.set('15429', 'name', 'Gorseval the Multifarious')
    file.set('15429', 'icon', 'resources/graphics/bosses/gorseval_the_multifarious.png')

    file.add_section('15375')
    file.set('15375', 'post', 'true')
    file.set('15375', 'name', 'Sabetha the Saboteur')
    file.set('15375', 'icon', 'resources/graphics/bosses/sabetha_the_saboteur.png')

    # WING 2
    file.add_section('16123')
    file.set('16123', 'post', 'true')
    file.set('16123', 'name', 'Slothasor')
    file.set('16123', 'icon', 'resources/graphics/bosses/slothasor.png')

    file.add_section('16088,16137,16125')
    file.set('16088,16137,16125', 'post', 'true')
    file.set('16088,16137,16125', 'name', 'Prison Camp')
    file.set('16088,16137,16125', 'icon', 'resources/graphics/bosses/prison_camp.png')

    file.add_section('16115')
    file.set('16115', 'post', 'true')
    file.set('16115', 'name', 'Matthias Gabrel')
    file.set('16115', 'icon', 'resources/graphics/bosses/matthias_gabrel.png')

    # WING 3
    file.add_section('16235')
    file.set('16235', 'post', 'true')
    file.set('16235', 'name', 'Keep Construct')
    file.set('16235', 'icon', 'resources/graphics/bosses/keep_construct.png')

    file.add_section('16247')
    file.set('16247', 'post', 'true')
    file.set('16247', 'name', 'Twisted Castle')
    file.set('16247', 'icon', 'resources/graphics/bosses/twisted_castle.png')

    file.add_section('16246,16286')
    file.set('16246,16286', 'post', 'true')
    file.set('16246,16286', 'name', 'Xera')
    file.set('16246,16286', 'icon', 'resources/graphics/bosses/xera.png')

    # WING 4
    file.add_section('17194')
    file.set('17194', 'post', 'true')
    file.set('17194', 'name', 'Cairn the Indomitable')
    file.set('17194', 'icon', 'resources/graphics/bosses/cairn_the_indomitable.png')

    file.add_section('17172')
    file.set('17172', 'post', 'true')
    file.set('17172', 'name', 'Mursaat Overseer')
    file.set('17172', 'icon', 'resources/graphics/bosses/mursaat_overseer.png')

    file.add_section('17188')
    file.set('17188', 'post', 'true')
    file.set('17188', 'name', 'Samarog')
    file.set('17188', 'icon', 'resources/graphics/bosses/samarog.png')

    file.add_section('17154')
    file.set('17154', 'post', 'true')
    file.set('17154', 'name', 'Deimos')
    file.set('17154', 'icon', 'resources/graphics/bosses/deimos.png')

    # WING 5
    file.add_section('19767')
    file.set('19767', 'post', 'true')
    file.set('19767', 'name', 'Soulless Horror')
    file.set('19767', 'icon', 'resources/graphics/bosses/soulless_horror.png')

    file.add_section('19828')
    file.set('19828', 'post', 'true')
    file.set('19828', 'name', 'River of Souls')
    file.set('19828', 'icon', 'resources/graphics/bosses/river_of_souls.png')

    file.add_section('19536')
    file.set('19536', 'post', 'true')
    file.set('19536', 'name', 'Eater of Souls')
    file.set('19536', 'icon', 'resources/graphics/bosses/eater_of_souls.png')

    file.add_section('19691')
    file.set('19691', 'post', 'true')
    file.set('19691', 'name', 'Broken King')
    file.set('19691', 'icon', 'resources/graphics/bosses/broken_king.png')

    file.add_section('19844,19651')
    file.set('19844,19651', 'post', 'true')
    file.set('19844,19651', 'name', 'Statue of Darkness')
    file.set('19844,19651', 'icon', 'resources/graphics/bosses/statue_of_darkness.png')

    file.add_section('19450')
    file.set('19450', 'post', 'true')
    file.set('19450', 'name', 'Voice in the Void')
    file.set('19450', 'icon', 'resources/graphics/bosses/voice_in_the_void.png')

    # WING 6
    file.add_section('43974,-21562')  # I don't know why the fuck I get -21562?
    file.set('43974,-21562', 'post', 'true')
    file.set('43974,-21562', 'name', 'Conjured Amalgamate')
    file.set('43974,-21562', 'icon', 'resources/graphics/bosses/conjured_amagmalgated.png')

    file.add_section('21105,21089')
    file.set('21105,21089', 'post', 'true')
    file.set('21105,21089', 'name', 'Twin Largos')
    file.set('21105,21089', 'icon', 'resources/graphics/bosses/twin_largos.png')

    file.add_section('21041,20934')
    file.set('21041,20934', 'post', 'true')
    file.set('21041,20934', 'name', 'Qadim')
    file.set('21041,20934', 'icon', 'resources/graphics/bosses/qadim.png')

    # WING 7
    file.add_section('21964')
    file.set('21964', 'post', 'true')
    file.set('21964', 'name', 'Cardinal Sabir')
    file.set('21964', 'icon', 'resources/graphics/bosses/cardinal_sabir.png')

    file.add_section('22006')
    file.set('22006', 'post', 'true')
    file.set('22006', 'name', 'Cardinal Adina')
    file.set('22006', 'icon', 'resources/graphics/bosses/cardinal_adina.png')

    file.add_section('22000')
    file.set('22000', 'post', 'true')
    file.set('22000', 'name', 'Qadim the Peerless')
    file.set('22000', 'icon', 'resources/graphics/bosses/qadim_the_peerless.png')

    # FRACTALS
    file.add_section('17021')
    file.set('17021', 'post', 'true')
    file.set('17021', 'name', 'MAMA')
    file.set('17021', 'icon', 'resources/graphics/bosses/mama.png')

    file.add_section('17028')
    file.set('17028', 'post', 'true')
    file.set('17028', 'name', 'Siax the Corrupted')
    file.set('17028', 'icon', 'resources/graphics/bosses/siax_the_corrupted.png')

    file.add_section('16948')
    file.set('16948', 'post', 'true')
    file.set('16948', 'name', 'Ensolyss of the Endless Torment')
    file.set('16948', 'icon', 'resources/graphics/bosses/ensolyss_of_the_endless_torment.png')

    file.add_section('17632,17637')
    file.set('17632,17637', 'post', 'true')
    file.set('17632,17637', 'name', 'Skorvald the Shattered')
    file.set('17632,17637', 'icon', 'resources/graphics/bosses/skorvald_the_shattered.png')

    file.add_section('17949')
    file.set('17949', 'post', 'true')
    file.set('17949', 'name', 'Artsariiv')
    file.set('17949', 'icon', 'resources/graphics/bosses/artsariiv.png')

    file.add_section('17759')
    file.set('17759', 'post', 'true')
    file.set('17759', 'name', 'Arkk')
    file.set('17759', 'icon', 'resources/graphics/bosses/arkk.png')

    file.add_section('23254')
    file.set('23254', 'post', 'true')
    file.set('23254', 'name', 'Ai, Keeper of the Peak')
    file.set('23254', 'icon', 'resources/graphics/bosses/ai_keeper_of_the_peak.png')

    # TODO: STRIKE MISSIONS

    with open(path, 'w') as file_stream:
        file.write(file_stream)


def newDiscordConfig(path: str):
    """ Creates default discordConfig.ini """
    file = ConfigParser()

    file.add_section('basic')
    file.set('basic', 'selectedServer', '-1')
    file.set('basic', 'displayName', '')
    file.add_section('emojis')

    emojis = defaultEmoji()
    for key in emojis:
        file.set('emojis', key, emojis[key])

    file.add_section('server')

    with open(path, 'w') as file_stream:
        file.write(file_stream)


def newBossStorage(path: str):
    """ Creates emtpy bossStorage.ini """
    with open(path, 'w') as file:
        file.write('')


def parseConfigFile(path: str) -> dict:
    """
    Accepts a config file and parses it to dict, change type to int and boolean if possible

    :param path: relative path to config file
    :return: formatted dict
    """
    file = ConfigParser()
    file.read(path)
    tempDict = {}
    for section in file.sections():
        tempDict[section] = {}
        for key in dict(file[section]):
            tempValue = file[section][key]
            if tempValue in ['true', 'True', 'false', 'False']:  # check value for bool
                value = tempValue in ['true', 'True']
            elif tempValue.lstrip('-').isdecimal():  # check value for integer
                value = int(tempValue)
            else:
                value = tempValue
            tempDict[section][key] = value
    return tempDict


def storeConfigObject(config: ConfigObject, basicConfig: dict, bossConfig: dict, discordConfig: dict):
    """ takes config dicts and stores them in configObject """
    serverListSeparator = '<->'  # name and url are separated by this string, no nesting allowed

    config.rootPath = basicConfig['explorer']['rootpath']
    config.pollingRate = basicConfig['explorer']['pollingrate']
    config.storageCount = basicConfig['storage']['count']
    config.userToken = basicConfig['log']['usertoken']
    config.anonymousLog = basicConfig['log']['anonymous']
    config.displayName = discordConfig['basic']['displayname']
    config.selectedServer = discordConfig['basic']['selectedserver']
    if discordConfig['server']:
        serverList = sorted(discordConfig['server'])
        for server in serverList:
            config.serverList.append(discordConfig['server'][server].split(serverListSeparator))
    config.emojis = discordConfig['emojis']
    config.boss = bossConfig


def saveNewConfig(config: ConfigObject, basicPath: str, bossPath: str, discordPath: str):
    """ Takes configObject and writes data to config files """
    # basicConfig
    basic = ConfigParser()
    basic.read(basicPath)
    basic.set('explorer', 'rootpath', config.rootPath)
    basic.set('explorer', 'pollingrate', str(config.pollingRate))
    basic.set('log', 'usertoken', config.userToken)
    basic.set('log', 'anonymous', str(config.anonymousLog).lower())
    with open(basicPath, 'w') as basicFile:
        basic.write(basicFile)

    # bossConfig
    boss = ConfigParser()
    boss.read(bossPath)
    for bossID in config.boss:
        boss.set(bossID, 'post', str(config.boss[bossID]['post']).lower())
    with open(bossPath, 'w') as bossFile:
        boss.write(bossFile)

    # discordConfig
    discord = ConfigParser()
    discord.read(discordPath)
    discord.set('basic', 'selectedserver', str(config.selectedServer))
    discord.set('basic', 'displayname', config.displayName)
    discord.remove_section('server')
    discord.add_section('server')
    index = 0
    for server in config.serverList:
        discord.set('server', str(index), f'{server[0]}<->{server[1]}')
        index += 1
    with open(discordPath, 'w') as discordFile:
        discord.write(discordFile)


def defaultEmoji() -> dict:
    """ dict of all needed emojis """
    return {
        'player': ':bust_in_silhouette:',
        'damage': ':crossed_swords:',
        'quickness': '<:quickness:776075657519693825>',
        'alacrity': '<:alacrity:776075657159376956>',
        'might': '<:might:776075657402646568>',
        'fury': '<:fury:776075657343402024>',
        'Spellbreaker': '<:warrior_spellbreaker:776075661537574913>',
        'Berserker': '<:warrior_berserker:776075661785694238>',
        'Warrior': '<:warrior:776075661559201802>',
        'Deadeye': '<:thief_deadeye:776075661710065664>',
        'Daredevil': '<:thief_daredevil:776075661685030923>',
        'Thief': '<:thief:776075661407158314>',
        'Renegade': '<:revenant_renegade:776075661516996629>',
        'Herald': '<:revenant_herald:776075661755547678>',
        'Revenant': '<:revenant:776075659519983688>',
        'Soulbeast': '<:ranger_soulbeast:776075661932101632>',
        'Druid': '<:ranger_druid:776075661575585842>',
        'Ranger': '<:ranger:776075661331922945>',
        'Scourge': '<:necro_scourge:776075661722517534>',
        'Reaper': '<:necro_reaper:776075661516472371>',
        'Necromancer': '<:necro:776075659864571955>',
        'Mirage': '<:mirage:776075660111118376>',
        'Chronomancer': '<:mesmer_chronomancer:776075661751484496>',
        'Mesmer': '<:mesmer:776075659646205964>',
        'Firebrand': '<:guardian_firebrand:776075660132352040>',
        'Dragonhunter': '<:guardian_dragonhunter:776075659574640680>',
        'Guardian': '<:guardian:776075659763122206>',
        'Scrapper': '<:engineer_scrapper:776075660010455050>',
        'Holosmith': '<:engineer_holosmith:776075661512540180>',
        'Engineer': '<:engineer:776075659000414229>',
        'Weaver': '<:ele_weaver:776075656986492959>',
        'Tempest': '<:ele_tempest:776075656928296971>',
        'Elementalist': '<:ele:776075657095413771>'
    }
