from django.urls import path, include
from . import views
urlpatterns = [
    path('price_list', views.current_price, name='price'),
]