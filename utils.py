"""Module to filter the data"""
from datetime import datetime, date, timedelta

# import openpyxl
from workalendar.europe import Belgium

START_HOUR = 6
STOP_HOUR = 20
WEEK_DAYS = (1, 2, 3, 4, 5)

UMONS_HOLIDAYS = {
    2023: {
        date(2023, 1, 2),
        date(2023, 1, 3),
        date(2023, 1, 4),
        date(2023, 1, 5),
        date(2023, 1, 6),
        date(2023, 9, 27),
        date(2023, 12, 26),
        date(2023, 12, 27),
        date(2023, 12, 28),
        date(2023, 12, 29),
    },
    2024: {
        date(2024, 1, 2),
        date(2024, 1, 3),
        date(2024, 1, 4),
        date(2024, 1, 5),
        date(2024, 9, 27),
        date(2024, 12, 23),
        date(2024, 12, 24),
        date(2024, 12, 26),
        date(2024, 12, 27),
        date(2024, 12, 30),
        date(2024, 12, 31),
    },
    2025: {
        date(2025, 1, 2),
        date(2025, 1, 3),
        date(2025, 9, 27),
        date(2025, 12, 22),
        date(2025, 12, 23),
        date(2025, 12, 24),
        date(2025, 12, 26),
        date(2025, 12, 29),
        date(2025, 12, 30),
        date(2025, 12, 31),
    },
}


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

    if current_date in UMONS_HOLIDAYS.get(_year, []):
        return True

    return False


def is_an_holiday(_datetime: datetime, include_umons_holidays: bool = True) -> bool:
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

    if current_date in UMONS_HOLIDAYS.get(_year, []) and include_umons_holidays:
        return True

    return False


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
