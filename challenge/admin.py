from django.contrib import admin

from .models import Submission, Simulation, Result
# Register your models here.

admin.site.register(Simulation)
admin.site.register(Submission)
admin.site.register(Result)
