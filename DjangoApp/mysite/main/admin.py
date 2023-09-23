from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Patient,Record,ImageModel,User,DailyPatients
# Register your models here.

admin.site.register(Patient)
admin.site.register(Record)
admin.site.register(ImageModel)
admin.site.register(DailyPatients)
admin.site.register(User, UserAdmin)