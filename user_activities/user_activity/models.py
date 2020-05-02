from django.db import models

class User(models.Model):
    user_id = models.CharField(max_length=200,primary_key=True)
    real_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    tz = models.CharField(max_length=200)
    
    def __str__(self):
        return (self.user_id+', '+self.real_name)


class Activities(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()