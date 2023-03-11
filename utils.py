import datetime
from dateutil.relativedelta import relativedelta
from flask import Flask, Blueprint


def str2date(
        date: str,
    ) -> datetime.date:
    return datetime.datetime.strptime(date, '%Y-%m-%d').date()


def today(
        output_str: bool = False,
        format: str = '%Y-%m-%d',
    ) -> datetime.date:
    today_date = datetime.date.today()
    if output_str:
        today_date = today_date.strftime(format)
    return today_date


def calc_age(
        birthdate: datetime.date,
        date: datetime.date = None,
    ) -> int:
    if type(birthdate) is str:
        birthdate = str2date(birthdate)
    if type(date) is str:
        date = str2date(date)
    date = today() if date is None else date
    age = relativedelta(date, birthdate).years
    return age


def register_routes(
        app: Flask,
        blueprints: list[Blueprint],
    ) -> None:
    for bp in blueprints:
        app.register_blueprint(bp)

