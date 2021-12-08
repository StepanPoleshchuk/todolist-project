from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)  # не обязательное к заполнению
    created = models.DateTimeField(auto_now_add=True)  # автозаполнение текущим временем, без возможности изменения
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    # внешний ключ, прикрепляем запись конкретному юзеру
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
