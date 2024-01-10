from enum import Enum


class Color(Enum):
    SYSTEM = '[color(217)]'
    SUCCESS = '[color(222)]'
    ERROR = '[color(160)]'


def ms_to_timestamp(ms: int) -> str:
    seconds, milliseconds = divmod(ms, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return '%s:%s:%s' % (
        str(hours).zfill(2),
        str(minutes).zfill(2),
        str(seconds).zfill(2),
    )
