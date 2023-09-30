from django.urls import path

from orders import views


urlpatterns = [
    path('make/', views.make_order_view)
]
