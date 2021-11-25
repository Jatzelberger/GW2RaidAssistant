import requests


def newUserToken() -> tuple[str, str]:
    try:
        r = requests.get('https://dps.report/getUserToken', timeout=3)
        if r.status_code == 200:
            return 'success', r.json()['userToken']
        else:
            return 'error', str(r.status_code)
    except Exception as e:
        return 'error', str(e)


class ReportService:
    def __init__(self, targetURL: str, userToken: str, anonymous: bool):
        self.targetURL = targetURL
        self.userToken = userToken
        self.anonymous = str(anonymous).lower()

    def uploadFile(self, logPath) -> tuple[str, dict]:
        file_extension = logPath.split('.')[-1]
        file_object = {'file': (f'log.{file_extension}', open(logPath, 'rb'), f'text/{file_extension}')}
        r = requests.post(f'{self.targetURL}?json=1&generator=ei&anonymous={self.anonymous}&userToken={self.userToken}',
                          files=file_object)
        return ('success', r.json()) if r.status_code == 200 else ('error', {'code': r.status_code})


class WebhookDataService:
    def __init__(self, url: str):
        self.url = url

    def getStrippedData(self) -> dict:
        r = requests.get(f'https://dps.report/getJson?permalink={self.url}')
        if r.status_code != 200:
            return {}
        else:
            unnecessary_keys = ['phases', 'mechanics', 'uploadLinks', 'skillMap', 'buffMap', 'damageModMap',
                                'personalBuffs',
                                'combatReplayMetaData']
            data = r.json()
            for key in unnecessary_keys:
                data.pop(key, None)
            return data
