from django.contrib import admin
from .models import Riddle, UserAnswer
# Register your models here.
admin.site.register(Riddle)
admin.site.register(UserAnswer)