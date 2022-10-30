from tkinter import Image
from django.contrib import admin
from .models import Patient,Record,ImageModel
# Register your models here.

admin.site.register(Patient)
admin.site.register(Record)
admin.site.register(ImageModel)