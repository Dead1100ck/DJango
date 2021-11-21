from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Client)
admin.site.register(Comment)
admin.site.register(Order)
admin.site.register(Team)
admin.site.register(Project)
admin.site.register(Employee)