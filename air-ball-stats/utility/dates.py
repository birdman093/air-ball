from datetime import date, datetime

def slashesStringToDate(date: str) -> date:
    return datetime.strptime(date, '%m/%d/%Y').date()  

def dateToSlashesString(date_obj: date) -> str:
    return date_obj.strftime('%m/%d/%Y')

def dateToDashesString(date_obj: date) -> str:
    return date_obj.strftime('%Y-%m-%d')