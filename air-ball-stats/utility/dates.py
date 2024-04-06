from datetime import date, datetime
import pytz

def slashesStringToDate(date: str) -> date:
    return datetime.strptime(date, '%m/%d/%Y').date()  

def dashesStringToDate(date: str) -> date:
    return datetime.strptime(date, '%Y-%m-%d').date()  

def dateToSlashesString(date_obj: date) -> str:
    return date_obj.strftime('%m/%d/%Y')

def dateToDashesString(date_obj: date) -> str:
    return date_obj.strftime('%Y-%m-%d')

def convertUTCtoPSTtoDashesString(utc_time_str: str) -> str:
    utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=pytz.utc)
    la_time = utc_time.astimezone(pytz.timezone('America/Los_Angeles'))
    return dateToDashesString(la_time)

def get_today_date_PST() -> date:
    local_timezone = pytz.timezone('America/Los_Angeles')  # Example: 'America/Los_Angeles'
    return datetime.now(local_timezone)