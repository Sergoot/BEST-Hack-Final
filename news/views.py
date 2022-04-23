from django.http import JsonResponse
from datetime import datetime, timedelta
from django.shortcuts import render
import json
import requests

from news.models import Category


def news(request, category_title):
    date = (datetime.now()- timedelta(days=7)).isoformat()
    data1 = []
    category = Category.objects.get(title=category_title)
    all_cats = Category.objects.all()
    print(all_cats)
    for cat in all_cats:
        print(cat.ru_title)
    url = 'https://newsapi.org/v2/everything?q=+{}&domains=www.rbc.ru&sortBy=publishedAt&apiKey=5f701fba0cc24685a498672a7c8754d8'
    data = requests.get(url.format(category.short, date)).json()
    print(data)
    print(url.format(category.short, date))
    # print(data)
    response = data['articles']
    for resp in response:
        source = resp['source']['name']
        title = resp['title']
        urlToImage = resp['urlToImage']
        content = resp['description']
        res_content = content.replace('<ol><li>', '')
        res_content_final=res_content.replace('</li><li>', '')
        date=resp['publishedAt']
        res_date = date.replace('T',' ')
        res_res_final = res_date.replace('Z','')
        data_dict = {
                     'source': source,
                     'title': title,
                     'url': urlToImage,
                     'content': res_content_final,
                     'date': res_res_final,
                     }
        data1.append(data_dict)
    context = {'data': data1, 'all_cats': all_cats}
    return render(request, 'news/news.html', context)

