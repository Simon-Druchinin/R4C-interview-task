from django.core.validators import validate_email
from django.core.exceptions import FieldError, FieldDoesNotExist


def validate_order_data(data: dict) -> dict:
    REQUIRED_FIELDS = ('email', 'robot_serial')
    
    for field in REQUIRED_FIELDS:
        if not data.get(field):
            raise FieldDoesNotExist(f"'{field}' is required field")
        
    data = {key:data[key] for key in REQUIRED_FIELDS}
    
    validate_email(data['email'])
    if len(data['robot_serial']) > 5:
        raise FieldError(f"'robot_serial' field length has exceeded max value (5)")
    
    return data
