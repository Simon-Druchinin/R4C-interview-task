import json
from datetime import datetime

from django.core import serializers
from django.forms import ValidationError
from django.http import JsonResponse, HttpRequest

from robots.models import Robot

from robots.validators import validate_robot_creation_data


def robot_create_view(request: HttpRequest):
    if request.method == 'POST':
        body = request.POST
        validated_data = validate_robot_creation_data(body)
        if not validated_data:
            raise ValidationError('Invalid input body')

        new_record = Robot.objects.create(**validated_data)
        new_record.save()
        
        # Date string to datetime object (inner django serializer requirement)
        date_format = '%Y-%m-%d %H:%M:%S'
        new_record.created = datetime.strptime(new_record.created, date_format)
        data = json.loads(serializers.serialize('json', [new_record]))
        
        return JsonResponse(data=data, safe=False, status=201)
