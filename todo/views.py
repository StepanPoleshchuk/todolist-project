from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # готовые формы
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required  # помечая этой функцией любую другую функуию мы разрешаем взаимодействие с ней только зарегистрированных

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

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error':'Ошибка в имени или пароле'})
        else:
            login(request, user)
            return redirect('currenttodos')  # на страницу с тасками

@login_required
def logoutuser(request):
    if request.method == 'POST':  # чтоб не было автоподгрузки ссылки в браузерах и автоматом не разлогинивалось
        logout(request)
        return redirect('home')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form':TodoForm()})
    else:  # внес и отправил на размещение
        try:  # ошибка введения кривых данных
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)  # сохраняем
            newtodo.user = request.user  # привязка объекта к пользователю
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form':TodoForm(), 'error':'Переданы неверные данные'})

@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos':todos})

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/completedtodos.html', {'todos':todos})

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)  # только пользователь которому принадлежит, связь по ключу

    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form, 'error':'неверные данные'})

@login_required
def completetodo(request, todo_pk):  # пометить выполненным
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()  # заполняет текущей датой и временем
        todo.save()
        return redirect('currenttodos')

@login_required
def returntodo(request, todo_pk):  # возврат таска в список текущих
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = None  # заполняет None
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):  # удалить
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')
