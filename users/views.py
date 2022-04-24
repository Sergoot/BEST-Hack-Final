from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect

# from exchangeapp.models import Portfolio
from currency.models import Portfolio
from news import views as news_views
from .forms import LoginForm, CustomUserCreationForm, ValueForm
# from exchangeapp import views as vgames
# Create your views here.
from .models import CustomUser

# выход из аккаунта/текущей сессии. Перебрасывате на страницу входа
def logout_view(request):
    logout(request)
    return redirect('/')

# Вход пользователя в аккаунт
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    return HttpResponse('Пользователь заблокирован')
            else:
                return HttpResponse('Данные введены неверно. Проверьте логин или пароль')
    else:
        if request.user.is_authenticated:
            return redirect('/')
        else:
            form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

# регистрация нового пользователя
def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            #создание нового пользователя
            new_user = user_form.save(commit=False)
            #Сохранение пароля
            new_user.set_password(user_form.cleaned_data['password1'])
            # Сохранение нового пользователя
            new_user.save()
            return render(request, 'users/register_done.html', {'new_user': new_user})
    else:
        user_form = CustomUserCreationForm()
    return render(request, 'users/1index.html', {'user_form': user_form})


# логика пополнения баланса пользователя
def money(request, pk):
    user = CustomUser.objects.get(pk=pk)
    if request.method == 'GET':
        form = ValueForm()
        context = {'user': user, 'form': form}
        return render(request, 'users/form.html', context)
    elif request.method == 'POST':
        user_pk = CustomUser.objects.get(pk=pk)
        money_value = float(request.POST['value'])
        user_pk.rub = float(user_pk.rub) + money_value
        user_pk.save()
        context = {'value': money_value, 'user': user_pk}
        return render(request, 'users/money_success.html', context)


# текущий портфель пользователя
def portfolio_page(request):
    total_port = 0
    portfolio = Portfolio.objects.filter(user=request.user)
    for port in portfolio:
        total_port += port.total_price
    total_rub = total_port + request.user.rub
    context = {'portfolio_list': portfolio, 'total_rub': total_rub}
    return render(request, 'users/portfolio.html', context)





