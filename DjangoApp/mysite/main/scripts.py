from .models import Patient,Record
import datetime

def checkIfUserAvailable(name):
    allNames = [x.name for x in Patient.objects.all()]
    print(allNames)
    return not name in allNames

def getLastRecord(id):
    return Patient.objects.get(id=id).record_set.last() 

def saveRecord(values,patient,id):
    new_rec = Record(reason = values["reason"],date = datetime.datetime.now(), patient = Patient.objects.get(id=id),
    tests = {"radiology":{},"lab":{}}, description = values["description"],diagnosis = values["diagnosis"],notes = values["notes"])
    new_rec.save()
    patient.record_set.add(new_rec)
    return new_rec