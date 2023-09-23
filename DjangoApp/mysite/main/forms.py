from django import forms
from .models import User

class LoginForm(forms.Form):
    name = forms.CharField(label = "name",max_length=300)
    password = forms.CharField(widget=forms.PasswordInput())

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150,required=True)
    password = forms.CharField(max_length=150,widget=forms.PasswordInput(),required=True)
    password_conf = forms.CharField(max_length=150,widget=forms.PasswordInput(),required=True)
    email = forms.EmailField(required=True)
    specialization = forms.ChoiceField(choices=User.Specialization.choices)

class CreatePatient(forms.Form):
    name = forms.CharField(label = "Name",max_length=200)
    birthday = forms.DateTimeField(widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'required': 'required'}))
    gender = forms.ChoiceField(choices=(("Male","Male"),("Female","Female")))
    habits = forms.CharField(label = "Habits",max_length=300)
    blood = forms.ChoiceField(choices=(("Not Set","Not Set"),("A Rh+","A Rh+"),("A Rh-","A Rh-"),("B Rh+","B Rh+"),
    ("B Rh-","B Rh-"),("AB Rh+","AB Rh+"),("AB Rh-","AB Rh-"),("O Rh+","O Rh+"),("O Rh-","O Rh-")),required=False)
    medicines = forms.CharField(label = "Medicines",max_length=300)
    allergies = forms.CharField(label = "Allergies",max_length=300)
    history = forms.CharField(label = "History",max_length=1000,widget=forms.Textarea(attrs={"rows":1,"cols":50}))

class CreateRecord(forms.Form):
    reason = forms.CharField(label = "Reason",max_length=200, widget = forms.Textarea(attrs={"rows":1,"cols":150}))
    description = forms.CharField(label = "Descriptipon",max_length=3000,widget=forms.Textarea(attrs={"rows":5,"cols":150}))
    diagnosis = forms.CharField(label="Diagnosis",max_length=3000,widget=forms.Textarea(attrs={"rows":5,"cols":150}))
    notes = forms.CharField(label="Notes",max_length=3000,widget=forms.Textarea(attrs={"rows":5,"cols":150}))
    lab = forms.BooleanField(required=False)
    radiology = forms.BooleanField(required=False)
    docs = [(x.id,'(' + x.specialization + ') ' + x.username) for x in User.objects.all()]
    docs.append(("None","None"))
    dr_name = forms.ChoiceField(choices=docs,initial=docs[-1])

class CreateTests(forms.Form):
    h_bpm = forms.IntegerField()
    glucose_level = forms.IntegerField()

class SelectTests(forms.Form):
    check = forms.CheckboxInput()
