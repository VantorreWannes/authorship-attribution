from abc import ABC
from datetime import datetime


class BaseDataClass(ABC):

    def __iter__(self):
        for key in self.__dict__:
            value = getattr(self, key)
            if isinstance(value, datetime):
                yield key, value.isoformat()
            else:
                yield key, value
