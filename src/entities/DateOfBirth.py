import datetime

class DateOfBirth():
    def __init__(self, date_str: str):
        self._date: datetime.datetime = None

        self.date = date_str
    
    @property
    def date(self):
        return self._date
    
    @date.setter
    def date(self, date: str):
        self._date = datetime.datetime.strptime(date, "%d/%m/%Y")
        
    def __str__(self):
        return datetime.datetime.strftime(self.date, "%d/%m/%Y")