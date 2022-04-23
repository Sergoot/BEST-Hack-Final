from django.urls import path, include
from . import views
urlpatterns = [
    path('news/<str:category_title>', views.news, name='news'),
]
