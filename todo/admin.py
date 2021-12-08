from django.contrib import admin
from .models import Todo

class TodoAdmin(admin.ModelAdmin):  # кастомизация интерфейса администратора
    readonly_fields = ('created',)  # добавляем поле

admin.site.register(Todo, TodoAdmin)
