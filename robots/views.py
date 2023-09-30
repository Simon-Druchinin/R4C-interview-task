import json
from datetime import datetime, timedelta

from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.forms import ValidationError
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.db.models import Count

from robots.models import Robot
from robots.validators import validate_robot_creation_data
from robots.services import export_robot_report_to_xlsx


@csrf_exempt
def robot_create_view(request: HttpRequest):
    if request.method == 'POST':
        body = request.POST
        validated_data = validate_robot_creation_data(body)
        if not validated_data:
            raise ValidationError('Invalid input body')

        validated_data['serial'] = f"{validated_data['model']}-{validated_data['version']}"
        new_record = Robot.objects.create(**validated_data)
        new_record.save()
        
        # Date string to datetime object (inner django serializer requirement)
        date_format = '%Y-%m-%d %H:%M:%S'
        new_record.created = datetime.strptime(new_record.created, date_format)
        data = json.loads(serializers.serialize('json', [new_record]))
        
        return JsonResponse(data=data, safe=False, status=201)

def robot_report_view(request: HttpRequest):
    if request.method == 'GET':
        today = datetime.today().strftime('%Y-%m-%d 23:59:59')
        week_ago = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
        robots = (Robot.objects.all()
            .filter(created__range=[week_ago, today])
            .values('model', 'version')
            .annotate(week_amount=Count('model'))
            .order_by('model')
        )
        
        buffer = export_robot_report_to_xlsx(robots)
        response = HttpResponse(
            content_type="applicaiton/vnd.ms-excel",
            headers={"Content-Disposition": 'attachment; filename="robots_report.xlsx"'},
        )
        response.write(buffer.getvalue())
       
        return response
        
