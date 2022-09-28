from django.contrib import admin
from .models import Patient,Record
# Register your models here.

admin.site.register(Patient)
admin.site.register(Record)