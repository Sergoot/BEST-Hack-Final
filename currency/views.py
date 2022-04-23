from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
import requests
# Create your views here.
from bs4 import BeautifulSoup
from django.views.decorators.http import require_POST
from currency.forms import ValueForm
from currency.models import Currency, Portfolio


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
                                'ru_title': cur.ru_title,
                                'name': cur_name,
                                'price': cur_price,
                                'id': cur.id,

                                }
                    data.append(data_cur)
    context = {'data': data,}
    return render(request, 'currency/currency.html', context)


def buy_page(request, currency_id):
    currency = Currency.objects.get(pk=currency_id)
    buy_form = ValueForm()
    return render(request, 'currency/buy.html', {'form': buy_form, 'currency': currency})


def sell_page(request, currency_id):
    currency = Currency.objects.get(pk=currency_id)
    sell_form = ValueForm()
    return render(request, 'currency/sell.html', {'form': sell_form,'currency': currency})


@require_POST
def buy(request, currency_id):
    quantity = request.POST['value']
    currency = Currency.objects.get(pk=currency_id)
    user = request.user
    try:
        portfolio = Portfolio.objects.get(user=request.user, currency=currency)
    except Portfolio.DoesNotExist:
        portfolio = Portfolio.objects.create(user=request.user, currency=currency)
    if (float(user.rub) - int(quantity)*float(currency.price)) < 0:
        return HttpResponse('На балансе не достаточно средств, пополните баланс:<ссылка на пополнение>')
    user.rub = float(user.rub) - int(quantity)*float(currency.price)
    user.save()
    portfolio.quantity = int(portfolio.quantity)+int(quantity)
    portfolio.total_price = float(portfolio.total_price)+float(currency.price)*int(quantity)
    portfolio.save()
    return redirect('price')


@require_POST
def sell(request,currency_id):
    quantity = request.POST['value']
    currency = Currency.objects.get(pk=currency_id)
    user = request.user
    try:
        portfolio = Portfolio.objects.get(user=request.user, currency=currency)
    except Portfolio.DoesNotExist:
        return HttpResponse('Вы продаете больше акций, чем покупаете')
    if (int(portfolio.quantity)-int(quantity)) < 0:
        return HttpResponse('Вы продаете больше акций, чем покупаете')
    user.rub = float(user.rub) + int(quantity)*float(currency.price)
    user.save()
    portfolio.quantity = int(portfolio.quantity)-int(quantity)
    portfolio.total_price = float(portfolio.total_price) - float(currency.price) * int(quantity)
    portfolio.save()
    return redirect('price')


