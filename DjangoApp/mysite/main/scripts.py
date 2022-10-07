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

def orderPatients(all):
# This function uses the selection sort which has a O(n^2) complexity.I'll keep this during the development stage, however I can
# switch to a more efficient algorithm in the future.
    p_with_rec = []
    p_wo_rec = []
    for x in all: # Seperate patients with a record from the ones who don't
        if(getLastRecord(x.id) != None):
            p_with_rec.append(x)
        else:
            p_wo_rec.append(x)
    for o_val in range(0,len(p_with_rec)):
        big_Index = o_val #Stores the index of the most recent record
        big_val = getLastRecord(p_with_rec[o_val].id).date #Stores the date of the most recent record
        for i_val in range(o_val,len(p_with_rec)):
            if getLastRecord(p_with_rec[i_val].id).date > big_val:
                big_val = getLastRecord(p_with_rec[i_val].id).date
                big_Index = i_val
        p_with_rec[o_val] , p_with_rec[big_Index] = p_with_rec[big_Index] , p_with_rec[o_val]
    return p_with_rec + p_wo_rec