from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.current_price, name='price'),
    path('buy_page/<int:currency_id>', views.buy_page, name='buy_page'),
    path('sell_page/<int:currency_id>', views.sell_page, name='sell_page'),
    path('buy/<int:currency_id>', views.buy, name='buy'),
    path('sell/<int:currency_id>', views.sell, name='sell'),
]