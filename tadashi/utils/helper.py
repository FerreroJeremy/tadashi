
def get_season():
    from datetime import date, datetime

    dummy_year = 2000  # dummy leap year to allow input X-02-29 (leap day)
    seasons = [('winter', (date(dummy_year, 1, 1), date(dummy_year, 3, 20))),
               ('spring', (date(dummy_year, 3, 21), date(dummy_year, 6, 20))),
               ('summer', (date(dummy_year, 6, 21), date(dummy_year, 9, 22))),
               ('autumn', (date(dummy_year, 9, 23), date(dummy_year, 12, 20))),
               ('winter', (date(dummy_year, 12, 21), date(dummy_year, 12, 31)))]

    now = date.today()
    now = now.replace(year=dummy_year)
    season = next(season for season, (start, end) in seasons if start <= now <= end)

    return season


def get_day_of_week():
    from datetime import date
    import calendar

    my_date = date.today()

    return calendar.day_name[my_date.weekday()]
