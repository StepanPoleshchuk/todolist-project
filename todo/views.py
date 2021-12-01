from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout

def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == 'GET':  # если это метод GET то идет на signup
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
    else:  # если это метод POST то создаем пользователя
        # POST возвращает словарь, вытаскиваем данные по ключу
        if request.POST['password1'] == request.POST['password2']:  # проверяем соответствие паролей при вводе
            try:  # проверка уникальности имени пользователи по ошибке
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])  # Встроенная функция для создания новых пользователей
                user.save()  # объект нужно сохранить, create_user его только создает
                login(request, user)
                return redirect('currenttodos')  # на страницу с тасками
            except IntegrityError:  # IntegrityError возбуждается при неуникальности имени пользователя
                return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Это имя пользователя уже используется, пожалуйста задайте новое.'})
        else:
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Пароли не совпадают.'})
            # сообщить о несоответствии паролей

def logoutuser(request):
    if request.method == 'POST':  # чтоб не было автоподгрузки ссылки в браузерах и автоматом не разлогинивалось
        logout(request)
        return redirect('home')

def currenttodos(request):
    return render(request, 'todo/currenttodos.html')
