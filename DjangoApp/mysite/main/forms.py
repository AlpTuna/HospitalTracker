from logging import PlaceHolder
import re
from django import forms

class CreatePatient(forms.Form):
    name = forms.CharField(label = "Name",max_length=200)
    age = forms.IntegerField()
    gender = forms.ChoiceField(choices=(("Male","Male"),("Female","Female")))
    habits = forms.CharField(label = "Habits",max_length=300)
    blood = forms.ChoiceField(choices=(("Not Set","Not Set"),("A Rh+","A Rh+"),("A Rh-","A Rh-"),("B Rh+","B Rh+"),
    ("B Rh-","B Rh-"),("AB Rh+","AB Rh+"),("AB Rh-","AB Rh-"),("O Rh+","O Rh+"),("O Rh-","O Rh-")),required=False)
    medicines = forms.CharField(label = "Medicines",max_length=300)
    allergies = forms.CharField(label = "Allergies",max_length=300)
    history = forms.CharField(label = "History",max_length=1000)

class CreateRecord(forms.Form):
    reason = forms.CharField(label = "Reason",max_length=200, widget = forms.Textarea(attrs={"rows":1,"cols":150}))
    description = forms.CharField(label = "Descriptipon",max_length=3000,widget=forms.Textarea(attrs={"rows":5,"cols":150}))
    diagnosis = forms.CharField(label="Diagnosis",max_length=3000,widget=forms.Textarea(attrs={"rows":5,"cols":150}))
    notes = forms.CharField(label="Notes",max_length=3000,widget=forms.Textarea(attrs={"rows":5,"cols":150}))
    lab = forms.BooleanField(required=False)
    radiology = forms.BooleanField(required=False)

class CreateTests(forms.Form):
    h_bpm = forms.IntegerField()
    glucose_level = forms.IntegerField()

class SelectTests(forms.Form):
    check = forms.CheckboxInput()
