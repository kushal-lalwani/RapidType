from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
class TestResult(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    wpm = models.FloatField()
    accuracy = models.FloatField()
    test_date = models.DateTimeField(auto_now_add=True)
    test_time = models.IntegerField(null=True, default=0)
    text_type = models.CharField(max_length=100, default='')
    
    