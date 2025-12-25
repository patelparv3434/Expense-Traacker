from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Addfunds(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Add = models.IntegerField()

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Reason = models.CharField(max_length=50)
    Amount = models.IntegerField()
    Date = models.DateTimeField(default=timezone.now)
