from django.db import models
from django.core import validators
from django.contrib.auth. models import User
from django.core.validators import MinValueValidator

class Myexpense(models.Model):   
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Expensename = models.CharField(max_length=50)
    ProfitAmount = models.IntegerField(validators=[MinValueValidator(0)])
    comment = models.TextField(max_length=500)
    # total_amount = models.FloatField(default=0.0)
    def __str__(self):
        return self.user.username + " " + self.Expensename