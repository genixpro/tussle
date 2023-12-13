import datetime


def convert_date_from_iso_format(date_string: str | None):
    """
    This function is used to convert dates coming from the API which are formatted in
    iso format into python datetime objects.
    :param date_string:
    :return:
    """
    if date_string is None:
        return None

    if date_string.endswith("Z"):
        date_string = date_string[:-1]

    return datetime.datetime.fromisoformat(date_string)

def create_default_datetime():
    d = datetime.datetime.now()

    # Round the microseconds down to nearest thousands, because otherwise we can get comparison
    # errors because the microseconds are slightly different after serializing to isoformat and
    # back. isoformat only goes to milliseconds, not microseconds.
    d = d.replace(microsecond=(d.microsecond // 1000) * 1000)

    return d
