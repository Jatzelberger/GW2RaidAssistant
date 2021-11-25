from discord_webhook.webhook import DiscordWebhook, DiscordEmbed
from resources.backend.configObject import ConfigObject
from datetime import datetime, timedelta
from math import ceil


class DiscordService:
    def __init__(self, data: dict, url: str, config: ConfigObject):
        self.data = data
        self.url = url
        self.targetURL = config.serverList[config.selectedServer][1]
        self.emojis = config.emojis
        self.displayName = config.displayName

        self.webhookName: str = 'ArcDPS Log'
        self.successColor: int = 0x007332
        self.failColor: int = 0x730000
        self.chars: dict = {
            'success': u'\u2714',
            'fail': u'\u2716',
            'healthBar_full': u'\u25B0',
            'healthBar_empty': u'\u25B1',
            'space': u'\u2800'
        }

        self.header: str = ''  # boss name, cm, success/fail
        self.boss: str = ''  # boss name, fight duration, health
        self.player: str = ''  # player profession, name, dps, quickness, alacrity, fury, might
        self.report: str = ''  # dps.report url and additional text
        self.footer: str = ''  # log author (display name)
        self.timestamp: int = 0  # timestamp in seconds

        self.__initWebhook()

    def __initWebhook(self):
        self.__setup()
        self.__header()
        self.__bossInfo()
        self.__playerInfo()
        self.__logInfo()
        self.__footer()
        self.__timestamp()

    def __setup(self):
        self.webhook = DiscordWebhook(
            url=self.targetURL,
            username='DPS Log',
        )

        self.embed = DiscordEmbed(color=(self.successColor if self.data['success'] else self.failColor))

    def __header(self):
        self.header = f'{self.data["fightName"]}    ' + self.chars['success' if self.data['success'] else 'fail']
        self.embed.set_author(
            name=self.header,
            url=self.url,
            icon_url=self.data['fightIcon'],
        )

    def __bossInfo(self):
        duration = self.data["duration"][0:7]

        self.embed.add_embed_field(
            name='> **BOSS INFO**',
            value=f'Duration: {duration}\n{self.__bossInfoFormatting()}',
            inline=False
        )

    def __playerInfo(self):
        header = f'> **PLAYER INFO**\n{self.__playerInfoHeader()}'
        self.embed.add_embed_field(
            name=header,
            value=self.__playerInfoData(),
            inline=False
        )

    def __logInfo(self):
        self.embed.add_embed_field(
            name='> **LINK**',
            value=self.url,
            inline=False,
        )

    def __footer(self):
        self.footer = f'Recorded by ' + (self.displayName if self.displayName != '' else self.data['recordedBy'])
        self.embed.set_footer(text=self.footer)

    def __timestamp(self):
        tempTime = datetime.strptime(self.data["timeEnd"][0:19], "%Y-%m-%d %H:%M:%S") + timedelta(hours=5)
        self.logTime = int((tempTime - datetime.utcfromtimestamp(0)).total_seconds())
        self.embed.set_timestamp(timestamp=self.logTime)

    def __bossInfoFormatting(self) -> str:
        # special cases
        prisonCampID = [16088, 16137, 16125]
        statueOfDarknessID = [19844, 19651]
        twinLargosID = [19844, 19651]

        if self.data['triggerID'] in prisonCampID:  # Prison Camp
            returnString = ''
            for target in self.data['targets']:
                if target['id'] in prisonCampID:
                    percentage = round(100 - float(target['healthPercentBurned']), 2)
                    returnString += f'**{target["name"]}:**\nHealth: {percentage}%\n' \
                                    f'{self.__bossInfoHealthBar(percentage)}\n'
            return returnString

        elif self.data['triggerID'] in statueOfDarknessID:  # Statue of Darkness (Eyes)
            returnString = ''
            for target in self.data['targets']:
                if target['id'] in statueOfDarknessID:
                    percentage = round(100 - float(target['healthPercentBurned']), 2)
                    returnString += f'**{target["name"]}:**\nHealth: {percentage}%\n' \
                                    f'{self.__bossInfoHealthBar(percentage)}\n'
            return returnString

        elif self.data['triggerID'] in twinLargosID:  # Twin Largos
            returnString = ''
            for target in self.data['targets']:
                if target['id'] in twinLargosID:
                    percentage = round(100 - float(target['healthPercentBurned']), 2)
                    returnString += f'**{target["name"]}:**\nHealth: {percentage}%\n' \
                                    f'{self.__bossInfoHealthBar(percentage)}\n'
            return returnString

        else:  # Other Bosses
            bossID = self.data['triggerID']
            for target in self.data['targets']:
                if target['id'] == bossID:
                    percentage = round(100 - float(target['healthPercentBurned']), 2)
                    return f'Health: {percentage}%\n{self.__bossInfoHealthBar(percentage)}'

    def __bossInfoHealthBar(self, percentage: float) -> str:
        length = 25
        tempBrackets = length * percentage / 100
        fullBrackets = ceil(tempBrackets)
        emptyBrackets = length - fullBrackets
        return self.chars['healthBar_full'] * fullBrackets + self.chars['healthBar_empty'] * emptyBrackets

    def __playerInfoHeader(self):
        s = self.chars['space']
        header = f'{s * 2} {self.emojis["player"]}{s * 13}{self.emojis["damage"]}{s * 3}{self.emojis["quickness"]}' \
                 f'{s * 3}{self.emojis["alacrity"]}{s * 3}{self.emojis["fury"]}{s * 2} {self.emojis["might"]}\n'
        return header

    def __playerInfoData(self):
        playerStats = {}
        for player in self.data['players']:
            if player['name'] not in ['Conjured Sword', "Saul D'Alessio", ]:  # filter for names
                name = player['name']
                professionName = player['profession'].lower()
                professionIcon = self.emojis[professionName] if professionName in self.emojis else ' '

                # total dps special cases
                prisonCampID = [16088, 16137, 16125]
                statueOfDarknessID = [19844, 19651]
                twinLargosID = [19844, 19651]

                dps = 0
                if self.data['triggerID'] in statueOfDarknessID or self.data['triggerID'] in twinLargosID:
                    dps = player['dpsTargets'][0][0]['dps'] + player['dpsTargets'][1][0]['dps']
                elif self.data['triggerID'] in prisonCampID:
                    dps = player['dpsTargets'][0][0]['dps'] \
                          + player['dpsTargets'][1][0]['dps'] \
                          + player['dpsTargets'][2][0]['dps']
                else:
                    dps = player['dpsTargets'][0][0]['dps']

                # buff uptime
                quicknessID = 1187
                alacrityID = 30328
                mightID = 740
                furyID = 725

                quickness = 0.0
                alacrity = 0.0
                might = 0.0
                fury = 0.0
                for buff in player['buffUptimes']:
                    if buff['id'] == quicknessID:
                        quickness = buff['buffData'][0]['uptime']
                    elif buff['id'] == alacrityID:
                        alacrity = buff['buffData'][0]['uptime']
                    elif buff['id'] == mightID:
                        might = buff['buffData'][0]['uptime']
                    elif buff['id'] == furyID:
                        fury = buff['buffData'][0]['uptime']

                # data to dictionary
                playerStats[name] = {
                    'dps': dps,
                    'professionIcon': professionIcon,
                    'quickness': quickness,
                    'alacrity': alacrity,
                    'fury': fury,
                    'might': might,
                }
        # Sort by DPS
        sortedPlayers = sorted(playerStats, key=lambda x: playerStats[x]['dps'], reverse=True)

        # Format data to string for webhook
        returnString = ''
        for player in sortedPlayers:
            quickness = '{0:.1f}%'.format(round(playerStats[player]['quickness'], 1)) \
                if playerStats[player]['quickness'] >= 10 \
                else '{0:.1f}%'.format(round(playerStats[player]['quickness'], 1))
            alacrity = '{0:.1f}%'.format(round(playerStats[player]['alacrity'], 1)) \
                if playerStats[player]['quickness'] >= 10 \
                else '{0:.1f}%'.format(round(playerStats[player]['alacrity'], 1))
            might = '{0:.1f}'.format(round(playerStats[player]['might'], 1)) \
                if playerStats[player]['quickness'] >= 10 \
                else '{0:.1f}'.format(round(playerStats[player]['might'], 1))
            fury = '{0:.1f}%'.format(round(playerStats[player]['fury'], 1)) \
                if playerStats[player]['quickness'] >= 10 \
                else '{0:.1f}%'.format(round(playerStats[player]['fury'], 1))

            returnString += playerStats[player]['professionIcon'] \
                            + '`' \
                            + player + (' ' * (21 - len(player) + 4 - len(str(playerStats[player]['dps'])))) \
                            + str(playerStats[player]['dps']) + (' ' * (7 - len(quickness))) \
                            + quickness + (' ' * (7 - len(alacrity))) \
                            + alacrity + (' ' * (7 - len(fury))) \
                            + fury + (' ' * (6 - len(might))) \
                            + might \
                            + '`\n'
        return returnString

    def sendWebhook(self):
        self.webhook.add_embed(self.embed)
        self.webhook.execute()
