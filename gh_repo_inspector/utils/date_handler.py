import pendulum
from babel.dates import format_datetime
from gh_repo_inspector.utils.logging_config import get_logger

logger = get_logger(__name__)

def parse_date_range(date_range_str):
    """
    Parses natural date range expressions using pendulum.
    Returns a tuple of (start_date, end_date) in UTC.
    """
    now = pendulum.now('UTC')
    
    if not date_range_str:
        date_range_str = "last 30 days"
        
    date_range_str = date_range_str.lower().strip()
    
    if date_range_str == "this year":
        start_date = now.start_of('year')
        end_date = now.end_of('year')
    elif date_range_str.startswith("last ") and " days" in date_range_str:
        try:
            days = int(date_range_str.split(" ")[1])
            start_date = now.subtract(days=days)
            end_date = now
        except (IndexError, ValueError):
            raise ValueError(f"Invalid date range format: {date_range_str}")
    elif " to " in date_range_str:
        try:
            parts = date_range_str.split(" to ")
            start_date = pendulum.parse(parts[0], strict=False).in_timezone('UTC')
            end_date = pendulum.parse(parts[1], strict=False).in_timezone('UTC')
        except Exception as e:
            raise ValueError(f"Could not parse date range '{date_range_str}': {e}")
    else:
        # Try generic pendulum parse if it's just a single date or unknown format
        try:
            start_date = pendulum.parse(date_range_str, strict=False).in_timezone('UTC')
            end_date = now
        except Exception as e:
            raise ValueError(f"Unsupported date range format: {date_range_str}")

    return start_date, end_date

def format_date_for_display(dt, locale='en_US'):
    """
    Formats the resolved date into a human-readable string using babel.
    """
    return format_datetime(dt, format='long', locale=locale)

def format_date_iso(dt):
    """
    Formats date in ISO-8601 for internal processing (like GitHub API).
    """
    return dt.to_iso8601_string()
