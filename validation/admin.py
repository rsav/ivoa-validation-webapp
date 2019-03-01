from django.contrib import admin
 
#  Register your models here.
from .models import Services, Errors
  
admin.site.register(Services)
admin.site.register(Errors)

