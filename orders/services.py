from django.core.mail import send_mail
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

from robots.models import Robot
from customers.models import Customer
from orders.models import Order


def send_order_mail(model: str, version: str, to_mail: list[str]):
    message_template = "Добрый день!"\
    f" Недавно вы интересовались нашим роботом <b>модели {model}, версии {version}</b>."\
    " Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами"
    
    subject = f"Оповещение о появлении в наличии модели {model}-{version}"
    
    send_mail(
        subject=subject,
        message=message_template,
        html_message=message_template,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=to_mail,
        fail_silently=False,
    )

@receiver(post_save, sender=Robot)
def examine_new_robots(instance, **kwargs):
    robots_amount = Robot.objects.filter(serial=instance.serial).count()
    if robots_amount == 1:
        orders = Order.objects.filter(robot_serial=instance.serial).select_related("customer")
        customers_emails = [order.customer.email for order in orders]
    
        if customers_emails:
            send_order_mail(instance.model, instance.version, customers_emails)
