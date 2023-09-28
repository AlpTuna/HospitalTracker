from .models import Patient,Record,ImageModel,User
from .encryption_util import encrypt,decrypt
from django.core import serializers
from .models import User,DailyPatients
from django import forms 
import tensorflow
import datetime
import numpy as np
import os
import cv2

def checkIfUserAvailable(name):
    allNames = [x.name for x in Patient.objects.all()]
    print(allNames)
    return not name in allNames

def GetPrediction(directory):
    # INPUT : Name of the image
    # OUTPUT: Result of the prediction (Or None if the model cannot be loaded)
    if os.path.exists('main/trained_model.h5'):
        model = tensorflow.keras.models.load_model('main/trained_model.h5') 
        filename2 = "media/" + directory
        #It's important to add main' bcs. OS starts searching from the outer directory
    
        image_size = 250
        categories = ['NORMAL','PNEUMONIA']

        image_array2 = cv2.imread(filename2,cv2.IMREAD_GRAYSCALE)
        new_array2 = cv2.resize(image_array2,(image_size,image_size))
        new_array2 = new_array2.reshape(-1,image_size,image_size,1)
        prediction = model.predict([new_array2])
        result = categories[int(prediction[0][0])]

        return result
    else:
        print("Couldn't find trained_model.h5")
        return None

def getLastRecord(id):
    return Patient.objects.get(id=id).record_set.last() 

def saveRecord(values,id,user):
    patient = Patient.objects.get(id = id)
    new_rec = Record(reason = values["reason"],date = datetime.datetime.now(), patient = patient,ref_dr_id = None,doctor_id=user.id,
    tests = {"radiology":{"verified":False},"lab":{"verified":False}}, description = values["description"],diagnosis = values["diagnosis"],notes = values["notes"])
    if values["dr_name"] != "None":
        new_rec.ref_dr_id = values["dr_name"]
    for x in values["radioTests"]:
        new_rec.tests["radiology"][x] = "Not Set!"
    for x in values["labTests"]:
        new_rec.tests["lab"][x] = "Not Set!"
    if len(values["labTests"]) == 0 and len(values["radioTests"]) == 0:
        new_rec.verified = True
    else:
        new_rec.verified = False

    new_rec.save()
    patient.record_set.add(new_rec)

    todays_record = DailyPatients.objects.filter(day = datetime.datetime.today(),doctor=user).first()
    if todays_record:
        todays_record.amount +=1
        todays_record.save()
    else:
        todays_record = DailyPatients.objects.create(doctor=user,day=datetime.datetime.today(),amount=1)
        todays_record.save()
    return new_rec

def CreateInsertTestForm(testsArray,allTests):
    field = {}
    for test in testsArray:
        testType = allTests[test]
        if testType == "int":
            field[test] = forms.IntegerField()
        elif testType == "file":
            field[test] = forms.ImageField()
    return type("tests",(forms.BaseForm,),{"base_fields":field})

def UpdateTests(rec_id,type,values):
    record = Record.objects.get(id=rec_id)
    print(type)
    if type == "lab":
        for x in values:
            record.tests[type][x] = values[x]
    else:
        for x in values:
            img = ImageModel.objects.create(title = values[x].name, img = values[x])
            serialized_obj = serializers.serialize('json', [ img ]) #Serializes the image model so that it can be saved inside the record
            img.save()
            record.tests[type][x] = serialized_obj
    record.tests[type]["verified"] = True
    print(record.get_attr())
    record.save()
    print(record.tests)
    

def orderPatients(all):
# This function uses the selection sort which has a O(n^2) complexity. I'll keep this during the development stage, however I can
# switch to a more efficient algorithm in the future.

    # TO-DO: THIS FUNCTION DOESN'T WORK WITH AN ARRAY OF SIZE 1. FIX THAT !!!

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

def login_script(values):
    #Return values   0 : Success - 1 : Incorrect Name - 2 : Incorrect Password
    if(len(User.objects.filter(username = values["name"])) == 0): #Another model with the same name
        return 1
    else:
        user = User.objects.filter(username = values["name"])[0]
        print(user)
    if(decrypt(user.password) != values["password"]):
        pass
        #return 2
    else:
        return user

def register(values):
    if values["password"] != values["password_conf"]: #Passwords not matching
        return 0
    if(len(User.objects.filter(username = values["username"]))>0): #Another model with the same name
        return 0
    if(len(values["password"])<=3): #If the password is shorter than or equal to 3 char. 
        return 0

    User.objects.create_user(username = values["username"],password=values["password"],email=values["email"],specialization = values["specialization"])    
    
    return 1