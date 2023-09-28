from django.urls import path

from robots import views

urlpatterns = [
    path('report/', views.robot_report_view),
]
