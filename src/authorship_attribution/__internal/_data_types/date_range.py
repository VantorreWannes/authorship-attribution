from datetime import datetime


class DateRange:
    def __init__(self, start: datetime, end: datetime):
        self.start: datetime = start
        self.end: datetime = end

    def __iter__(self):
        for key in self.__dict__:
            value = getattr(self, key)
            if isinstance(value, datetime):
                yield key, value.isoformat()
            else:
                yield key, value
