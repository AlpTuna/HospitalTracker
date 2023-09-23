from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    class Specialization(models.TextChoices):
        GeneralPractitioner = "General Practitioner", "General Practitioner"
        InternalMedicine = "Internal Medicine", "Internal Medicine"
        Dermatology = "Dermatology", "Dermatology"
        Pediatrics = "Pediatrics","Pediatrics"
        Gynecology = "Gynecology", "Gynecology"
        Cardiology = "Cardiology", "Cardiology"
        Laboratory = "Laboratory", "Laboratory"
    
    specialization = models.CharField(max_length = 50, choices=Specialization.choices)

    def save(self,*args,**kwargs):
        if not self.pk: # Checks if the user was already created
            return super().save(*args,**kwargs)

class Notification(models.Model):
    text = models.CharField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)
    read_status = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Patient(models.Model):
    name = models.CharField(max_length=100)
    birthday = models.DateField()
    gender = models.CharField(max_length=6, null=True,blank=True)
    habits = models.CharField(max_length=300, default="Not set")
    blood = models.CharField(max_length=10,null=True,blank=True,default="Not set")
    medicines = models.CharField(max_length=300,default="Not set")
    allergies = models.CharField(max_length=300,default="Not set")
    history = models.CharField(max_length=1000,default="Not set")
    doctors = models.ManyToManyField(User)

    def get_attr(self):
        return {"name":self.name,"birthday":self.birthday,"gender":self.gender,"habits":self.habits,"blood":self.blood,
        "medicines":self.medicines,"allergies":self.allergies,"history":self.history}

class Record(models.Model):
    doctor_id = models.IntegerField()
    patient = models.ForeignKey(Patient , on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)
    description = models.CharField(max_length=3000, default="Not set")
    tests = models.JSONField(default={"radiology":{"verified":False},"lab":{"verified":False}})
    diagnosis = models.CharField(max_length = 3000, default = "Not set")
    notes = models.CharField(max_length = 3000, default = "Not set")
    ref_dr_id = models.IntegerField(null = True)

    def get_attr(self):
        vals = {"date":self.date,"reason": self.reason,"description":self.description,"diagnosis":self.diagnosis,
        "notes":self.notes,"tests":self.tests}
        if self.ref_dr_id != None:
            vals["Reference Doctor"] = User.objects.get(id = self.ref_dr_id)
        return vals

class ImageModel(models.Model):
    title = models.CharField(max_length = 200)
    img = models.ImageField()
    def get_attr(self):
        return {"img":self.img,"title":self.title}
    
class DailyPatients(models.Model):
    doctor = models.ForeignKey(User,on_delete=models.CASCADE)
    day = models.DateField()
    amount = models.SmallIntegerField()