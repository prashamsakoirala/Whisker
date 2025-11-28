from enum import Enum

class CatAnimationEnum(str, Enum):
    IDLE = "idle"
    SLEEP = "sleep"

class CatEventEnum(str, Enum):
    FEED = "feed"
    PLAY = "play"

class CatItemEnum(str, Enum):
    TOY = "toy"
    FISH = "fish"

class CatStateEnum(str, Enum):
    HUNGER = "hunger"
    HAPPINESS = "happiness"