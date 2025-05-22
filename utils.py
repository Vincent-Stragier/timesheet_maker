"""Module to filter the data"""

import random
from datetime import date, datetime, timedelta

# import openpyxl
from workalendar.europe import Belgium

UMONS_HOLIDAYS = {
    2023: (
        (date(2023, 1, 2), "Récupération du 01/01/2023"),
        (date(2023, 1, 3), "Vacances d'hiver"),
        (date(2023, 1, 4), "Vacances d'hiver"),
        (date(2023, 1, 5), "Vacances d'hiver"),
        (date(2023, 1, 6), "Vacances d'hiver"),
        (date(2023, 9, 27), "Fête de la Communauté française"),
        (date(2023, 12, 26), "Noël second jour"),
        (date(2023, 12, 27), "Récupération du 11/11/2023"),
        (date(2023, 12, 28), "Vacances d'hiver"),
        (date(2023, 12, 29), "Vacances d'hiver"),
    ),
    2024: (
        (date(2024, 1, 2), "Vacances d'hiver"),
        (date(2024, 1, 3), "Vacances d'hiver"),
        (date(2024, 9, 27), "Fête de la Communauté française"),
        (date(2024, 12, 23), "Récupération du 21/07/2024"),
        (date(2024, 12, 24), "Vacances d'hiver"),
        (date(2024, 12, 26), "Noël second jour"),
        (date(2024, 12, 27), "Vacances d'hiver"),
        (date(2024, 12, 30), "Vacances d'hiver"),
        (date(2024, 12, 31), "Vacances d'hiver"),
    ),
    2025: (
        (date(2025, 1, 2), "Vacances d'hiver"),
        (date(2025, 1, 3), "Vacances d'hiver"),
        (date(2025, 9, 27), "Fête de la Communauté française"),
        (date(2025, 12, 22), "Récupération du 27/09/2025"),
        (date(2025, 12, 23), "Récupération du 01/11/2025"),
        (date(2025, 12, 24), "Vacances d'hiver"),
        (date(2025, 12, 26), "Noël second jour"),
        (date(2025, 12, 29), "Vacances d'hiver"),
        (date(2025, 12, 30), "Vacances d'hiver"),
        (date(2025, 12, 31), "Vacances d'hiver"),
    ),
}

TRANSLATIONS = {
    "New year": "Nouvel an",
    "Easter Monday": "Lundi de Pâques",
    "Labour Day": "Fête du travail",
    "Ascension Thursday": "Jeudi de l'Ascension",
    "Whit Monday": "Lundi de Pentecôte",
    "National Day": "Fête nationale",
    "Assumption of Mary to Heaven": "Assomption",
    "All Saints Day": "Toussaint",
    "Armistice of 1918": "Armistice (1918)",
    "Christmas Day": "Noël",
}


def get_umons_holidays_by_year(year: int) -> list:
    """Get the UMONS holidays for a given year.

    Args:
        year (int): the year.

    Returns:
        list: the list of holidays.
    """
    umons_holidays = UMONS_HOLIDAYS.get(year, [])
    return list(map(lambda x: x[0], umons_holidays))


def get_work_holidays_by_year(year: int) -> list:
    """Get the work holidays for a given year.

    Args:
        year (int): the year.

    Returns:
        list: the list of holidays.
    """

    year_holidays = get_work_holidays_by_year.all_holidays.get(year)

    if year_holidays is None:
        year_holidays = [date for date, _ in Belgium().holidays(year)]
        get_work_holidays_by_year.all_holidays[year] = year_holidays

    return year_holidays


get_work_holidays_by_year.all_holidays = {}


def is_an_umons_holiday(_datetime: datetime) -> bool:
    """Check if the datetime element is part of an UMONS holiday.

    Args:
        _datetime (datetime): the datetime object.

    Returns:
        bool: return True if the datetime is an UMONS holiday. False otherwise.
    """
    _year = _datetime.year

    current_date = _datetime.date()

    if current_date in get_umons_holidays_by_year(_year):
        return True

    return False


def is_an_holiday(
    _datetime: datetime, include_umons_holidays: bool = True
) -> bool:
    """Check if the datetime element is part of an holiday.

    Args:
        _datetime (datetime): the datetime object.

    Returns:
        bool: return True if the datetime is an holiday. False otherwise.
    """
    _year = _datetime.year

    current_date = _datetime.date()

    if current_date in get_work_holidays_by_year(_year):
        return True

    if (
        current_date in get_umons_holidays_by_year(_year)
        and include_umons_holidays
    ):
        return True

    return False


def get_holiday_name(_datetime: datetime) -> str:
    """Get the name of the holiday for the given date.

    Args:
        _datetime (datetime): the datetime object.

    Returns:
        str: the name of the holiday.
    """
    _year = _datetime.year

    current_date = _datetime.date()

    for holiday in Belgium().holidays(_year):
        if holiday[0] == current_date:
            return TRANSLATIONS.get(holiday[1], holiday[1])

    for holiday in UMONS_HOLIDAYS.get(_year, []):
        if holiday[0] == current_date:
            return holiday[1]

    return ""


def is_weekend(_datetime: datetime) -> bool:
    """Check if the datetime is during the weekend.

    Args:
        _datetime (datetime): the datetime object.

    Returns:
        bool: return True is the datetime is during the weekend.
    """
    return _datetime.isoweekday() in (6, 7)


def is_an_holiday_to_recover(_datetime: datetime) -> bool:
    """Check if the datetime is an holiday to recover (during a weekend).

    Args:
        _datetime (datetime): the datetime object.

    Returns:
        bool: return True if the datetime is an holiday to recover. False otherwise.
    """
    return is_an_holiday(_datetime) and is_weekend(_datetime)


def get_weekends_holidays_and_umons_holidays_for_year(year: int) -> list:
    """Get the list of weekends, holidays and UMONS holidays for a given year.

    Args:
        year (int): the year.

    Returns:
        list: the list of weekends, holidays and UMONS holidays.
    """
    weekends = []
    holidays = []
    umons_holidays = []
    # to_recover = []

    for month in range(1, 13):
        for day in range(1, 32):
            try:
                _datetime = datetime(year, month, day)

                if is_weekend(_datetime):
                    weekends.append(_datetime)

                if is_an_holiday(_datetime, include_umons_holidays=False):
                    holidays.append(_datetime)

                # if is_an_holiday_to_recover(_datetime):
                #     to_recover.append(_datetime)

                if is_an_umons_holiday(_datetime):
                    umons_holidays.append(_datetime)

            except ValueError:
                break

    return weekends, holidays, umons_holidays


def last_day_of_month(_datetime: datetime) -> datetime:
    """Return the last day of the month for the given date.

    Args:
        _datetime (datetime.datetime): the date for which we want to get the last day of the month.

    Returns:
        datetime.datetime: the last day of the month.
    """
    _datetime = _datetime.replace(day=28) + timedelta(days=4)
    return _datetime - timedelta(days=_datetime.day)


def number_of_days_in_month(year: int, month: int) -> int:
    """Return the number of days in the given month.

    Args:
        year (int): the year of the month.
        month (int): the month for which we want to get the number of days.

    Returns:
        int: the number of days in the given month.
    """
    return last_day_of_month(datetime(year, month, 1)).day


def get_description(
    current_date: datetime,
    first_day: int,
    last_day: int,
    year: int,
    researcher_holidays: list,
    sick_days: list = None,
):
    """Generate the description for a given date.

    Args:
        date (datetime.datetime): The date to generate the description for.
        first_day (int): The first day of the month.
        last_day (int): The last day of the month.
        year (int): The year of the date.
        researcher_holidays (list): The list of researcher holidays.
        sick_days (list): The list of sick days.

    Returns:
        str: The description for the given date.
    """
    weekends, work_holidays, umons_holidays = (
        get_weekends_holidays_and_umons_holidays_for_year(year)
    )

    name = get_holiday_name(current_date)
    day = current_date.day

    if last_day < day or first_day > day:
        return "Hors convention", day in weekends

    if current_date in weekends:
        return "Weekend", True

    if current_date in work_holidays:
        return f"JF - {name}", day in weekends

    if current_date in umons_holidays:
        if name.startswith("Récupération") or name.startswith(
            "Fête de la Communauté française"
        ):
            return f"{name}", day in weekends
        return f"Congé UMONS - {name}", day in weekends

    if current_date in researcher_holidays:
        return "Congé chercheur", day in weekends

    if sick_days:
        if current_date in sick_days:
            return "Congé maladie", day in weekends

    return "", day in weekends


def get_random_hours_per_day(
    min_hours: float, max_hours: float, under_min_probability: float
):
    """Get a random number of hours per day.

    Args:
        min_hours (float): The minimum number of hours per day.
        max_hours (float): The maximum number of hours per day.
        under_min_probability (float): The probability of getting a number of hours per day under the minimum.

    Returns:
        float: The number of hours per day.
    """
    duration = random.uniform(min_hours, max_hours)
    half_probability = under_min_probability / 2

    if (
        not (half_probability < random.random() < 1 - half_probability)
        and under_min_probability > 0
    ):
        return (min_hours / max_hours) * 0.99 * duration

    return duration


def get_work_days_duration(
    number_of_days: int,
    number_of_half_days: int,
    min_hours: float,
    max_hours: float,
    quota: float = 1,
    under_min_probability: float = 0.05,
    time_increment: float = 0.5,
) -> list:
    """Get the duration of work days.

    Args:
        number_of_days (int): The number of days to get the duration for.
        number_of_half_days (int): The number of half days to get the duration for.
        min_hours (float): The minimum number of hours per day.
        max_hours (float): The maximum number of hours per day.
        quota (float): The quota of the researcher.
        under_min_probability (float): The probability of getting a number of hours per day under the minimum.
        time_increment (float): The time increment.

    Returns:
        list: The list of durations for the work days.
    """

    def _hours_per_day(
        _number_of_days: int = number_of_days,
        _min_hours: float = min_hours,
        _max_hours: float = max_hours,
        _under_min_probability: float = under_min_probability,
    ) -> list:
        """Get the hours per day.

        Args:
            number_of_days (int): The number of days to get the hours for.

        Returns:
            list: The list of hours per day.
        """
        hours_per_day = [
            get_random_hours_per_day(
                _min_hours,
                _max_hours,
                _under_min_probability,
            )
            for _ in range(_number_of_days)
        ]

        return [
            round((hour * quota) / time_increment) * time_increment
            for hour in hours_per_day
        ]

    # Full days
    mean_duration = 0
    while mean_duration < (min_hours + 0.1 * (max_hours - min_hours)) * quota:
        durations = _hours_per_day(number_of_days)
        mean_duration = sum(durations) / number_of_days

    # Half days
    half_days_mean = 0
    while (
        half_days_mean
        < (min_hours + 0.1 * (max_hours - min_hours)) * quota / 2
    ):

        if number_of_half_days == 0:
            half_days_durations = []
            break

        half_days_durations = _hours_per_day(
            number_of_half_days,
            min_hours / 2,
            max_hours / 2,
            under_min_probability,
        )
        half_days_mean = sum(half_days_durations) / number_of_half_days

    return durations, half_days_durations


def get_number_of_working_days(
    year: int,
    month: int,
    first_day: int,
    last_day: int,
    researcher_holidays: list,
    half_days: list = None,
    sick_days: list = None,
):
    """Get the number of working days in a month.

    Args:
        year (int): The year of the month.
        month (int): The month to get the number of working days for.
        first_day (int): The first day of the month.
        last_day (int): The last day of the month.
        researcher_holidays (list): The list of researcher holidays.
        sick_days (list): The list of sick days.

    Returns:
        tuple: The number of working days and the number of half days.
    """
    number_of_days = 0
    number_of_half_days = 0

    weekends, work_holidays, umons_holidays = (
        get_weekends_holidays_and_umons_holidays_for_year(year)
    )

    for day in range(first_day, last_day + 1):
        current_date = datetime(year, month, day)
        if current_date in weekends:
            continue

        if current_date in work_holidays:
            continue

        if current_date in umons_holidays:
            continue

        if current_date in researcher_holidays:
            continue

        if sick_days is not None:
            if current_date in sick_days:
                continue

        if half_days is not None:
            if current_date in half_days:
                number_of_half_days += 1
                continue

        number_of_days += 1

    return number_of_days, number_of_half_days


# def copy_sheet_with_styles(source_sheet, dest_sheet):
#     """Copy the content and styles from a source sheet to a destination sheet.

#     Args:
#         source_sheet (openpyxl.worksheet.worksheet.Worksheet): the source sheet.
#         dest_sheet (openpyxl.worksheet.worksheet.Worksheet): the destination sheet.
#     """
#     for row in source_sheet.iter_rows():
#         for cell in row:
#             _has_style = False
#             if isinstance(cell, openpyxl.cell.cell.Cell):
#                 _has_style = cell.has_style

#             if cell.value is not None or _has_style:  # Check for non-empty or styled cells
#                 # Copy cell value
#                 dest_cell = dest_sheet[cell.coordinate]
#                 dest_cell.value = cell.value

#                 # Copy cell styles
#                 if _has_style:
#                     dest_cell.font = cell.font
#                     dest_cell.fill = cell.fill
#                     dest_cell.border = cell.border
#                     dest_cell.alignment = cell.alignment
#                     dest_cell.number_format = cell.number_format
#                     dest_cell.protection = cell.protection

#     # Copy column widths
#     for col_letter, column_dimension in source_sheet.column_dimensions.items():
#         if column_dimension.width:
#             dest_sheet.column_dimensions[col_letter].width = column_dimension.width

#     # Copy row heights
#     for row_number, row_dimension in source_sheet.row_dimensions.items():
#         if row_dimension.height:
#             dest_sheet.row_dimensions[row_number].height = row_dimension.height
