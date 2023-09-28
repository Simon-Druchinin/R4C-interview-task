from django.http import HttpRequest
from django.shortcuts import request

from robots.models import Robot

def robot_report_view(request: HttpRequest):
    if request.method == 'GET':
        ...
