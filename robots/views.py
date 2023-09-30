from datetime import datetime, timedelta

from django.http import HttpRequest, HttpResponse
from django.db.models import Count

from robots.models import Robot
from robots.services import export_robot_report_to_xlsx

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
        
