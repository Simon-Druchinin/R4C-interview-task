from datetime import datetime
from django.core.exceptions import FieldError, FieldDoesNotExist


def validate_robot_creation_data(data: dict) -> dict:
    REQUIRED_FIELDS = ('model', 'version', 'created')
    
    for field in REQUIRED_FIELDS:
        if not data.get(field):
            raise FieldDoesNotExist(f"'{field}' is required field")
        
    data = {key:data[key] for key in REQUIRED_FIELDS}
    
    if len(data['model']) > 2:
        raise FieldError(f"'model' field length has exceeded max value (2)")
    elif len(data['version']) > 2:
        raise FieldError(f"'version' field length has exceeded max value (2)")
    
    date_format = '%Y-%m-%d %H:%M:%S'
    try:
        datetime.strptime(data['created'], date_format)
    except ValueError:
        raise FieldError("Incorrect data format, should be YYYY-MM-DD HH:MM:SS")
    
    return data
