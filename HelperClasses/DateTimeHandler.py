import datetime


class DateTimeHandler(datetime.datetime):

    datetime_formate = "%Y-%m-%dT%H:%M:%S"
    date_fromate = "%Y-%m-%d"
    time_formate = "%H:%M:%S"

    @classmethod
    def string_to_date(cls, date_string):
        return DateTimeHandler.strptime(string=date_string, format=DateTimeHandler.date_fromate)

    @classmethod
    def string_to_time(cls, time_string):
        return DateTimeHandler.strptime(string=time_string, format=DateTimeHandler.time_formate)

    @classmethod
    def string_to_datetime(cls, datetime_string):
        return DateTimeHandler.strptime(string=datetime_string, format=DateTimeHandler.datetime_formate)
