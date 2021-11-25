from dataclasses import dataclass
from datetime import datetime


@dataclass
class BossObject:
    id: int  # unique boss ID
    time: datetime  # log creation time
    path: str  # explorer path to file
    name: str = 'Loading...'  # boss name
    icon: str = 'resources/graphics/bosses/loading.png'  # bossIcon
    cm: bool = False  # CM active
    success: bool = None  # success or fail
    old: bool = False  # log loaded from last session
    url: str = ''  # dps.report permalink
    webhook: bool = False
    widgetID = None  # unique widgetID to edit boss properties
