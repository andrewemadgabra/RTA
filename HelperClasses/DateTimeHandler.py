import datetime


class DateTimeHandler(datetime.datetime):

    datetime_formate = "%Y-%m-%dT%H:%M:%S"
    date_fromate = "%Y-%m-%d"
    time_formate = "%H:%M:%S"

    @classmethod
    def string_to_date(cls, date_string):
        return DateTimeHandler.strptime(date_string, DateTimeHandler.date_fromate).date()

    @classmethod
    def string_to_time(cls, time_string):
        return DateTimeHandler.strptime(time_string, DateTimeHandler.time_formate).time()

    @classmethod
    def string_to_datetime(cls, datetime_string):
        return DateTimeHandler.strptime(datetime_string, DateTimeHandler.datetime_formate)
