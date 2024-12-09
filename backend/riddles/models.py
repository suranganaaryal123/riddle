import django
from django.db import models

#this stores the questions and their respective answer
class Riddle(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question

#this stores the user who answered the questionas in their name, their answer and whether it was correct or not and has
# a foreign relationship with the riddle table

class UserAnswer(models.Model):
    user_name = models.CharField(max_length=100)  
    riddle = models.ForeignKey(Riddle, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer to {self.riddle.question} by {self.user_name}"
