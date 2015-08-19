from django.contrib import admin

from .models import Challenge,Submission, Dataset, Result
# Register your models here.

class SubmissionAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)

admin.site.register(Challenge)
admin.site.register(Dataset)
admin.site.register(Submission,SubmissionAdmin)
admin.site.register(Result)
