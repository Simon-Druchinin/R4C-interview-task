from django.urls import path

from robots import views

urlpatterns = [
    path('create/', views.robot_create_view),
    path('report/', views.robot_report_view),
]
