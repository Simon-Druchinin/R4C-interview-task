import json

from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpRequest

from customers.models import Customer

from robots.models import Robot

from orders.models import Order
from orders.validators import validate_order_data
from orders.services import send_order_mail


@csrf_exempt
def make_order_view(request: HttpRequest):
    if request.method == 'POST':
        body = request.POST
        data = validate_order_data(body)
        
        customer, _ = Customer.objects.get_or_create(email=data['email'])
        robot_serial_exists = Robot.objects.filter(serial=data['robot_serial']).exists()
        
        if robot_serial_exists:
            response_data = {"success": True, "detail": "Робот есть в наличии"}
        else:
            order, created = Order.objects.get_or_create(customer=customer, robot_serial=data['robot_serial'])
            
            response_data = {"success": True, "detail": "Ваша заявка уже находится в списке заказов - ожидайте"}
            if created:
                response_data = {"success": True, "detail": "Ваша заявка была добавлена в список заказов - ожидайте"}
            
        return JsonResponse(data=response_data, safe=False, status=200, json_dumps_params={'ensure_ascii': False})
