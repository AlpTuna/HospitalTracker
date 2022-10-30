from django.db import models

# Create your models here.
class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=6, null=True,blank=True)
    habits = models.CharField(max_length=300, default="Not set")
    blood = models.CharField(max_length=10,null=True,blank=True,default="Not set")
    medicines = models.CharField(max_length=300,default="Not set")
    allergies = models.CharField(max_length=300,default="Not set")
    history = models.CharField(max_length=1000,default="Not set")


    def get_attr(self):
        return {"name":self.name,"age":self.age,"gender":self.gender,"habits":self.habits,"blood":self.blood,
        "medicines":self.medicines,"allergies":self.allergies,"history":self.history}



class Record(models.Model):
    patient = models.ForeignKey(Patient , on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)
    description = models.CharField(max_length=3000, default="Not set")
    tests = models.JSONField(default={"radiology":{"verified":False},"lab":{"verified":False}})
    diagnosis = models.CharField(max_length = 3000, default = "Not set")
    notes = models.CharField(max_length = 3000, default = "Not set")

    
    def get_attr(self):
        return {"date":self.date,"reason": self.reason,"description":self.description,"diagnosis":self.diagnosis,
        "notes":self.notes,"tests":self.tests}

class ImageModel(models.Model):
    title = models.CharField(max_length = 200)
    img = models.ImageField()
    def get_attr(self):
        return {"img":self.img,"title":self.title}