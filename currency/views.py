from django.http import JsonResponse
from django.shortcuts import render
import requests
# Create your views here.
from bs4 import BeautifulSoup

from currency.models import Currency


def current_price(request):

    data = []
    currencies = Currency.objects.all()
    url = 'https://finance.rambler.ru/currencies/'
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    currency_all = soup.find(name='div', attrs={'class': 'finance-currency-table__table'}).find_all(
        class_='finance-currency-table__tr')
    for currency in currency_all:
        name = currency.find(class_='finance-currency-table__cell finance-currency-table__cell--code')
        price = currency.find(class_='finance-currency-table__cell finance-currency-table__cell--value')
        if name != None and price != None:
            cur_name = name.text.replace("\n", '')
            cur_price = price.text.replace("\n", '')
            for cur in currencies:
                if cur.name == cur_name:
                    cur.price = float(cur_price)
                    cur.save()
                    data_cur = {
                                'name': cur_name,
                                'price': cur_price
                                }
                    data.append(data_cur)
    context = {'data': data}
    return render(request, 'currency/price_list.html', context)

