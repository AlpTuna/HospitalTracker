from ast import Param
from urllib import request
from xml.dom.minidom import Document
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import Patient,Record
from .forms import CreatePatient,CreateTests,SelectTests,CreateRecord
import datetime
from .scripts import checkIfUserAvailable,getLastRecord,saveRecord,orderPatients

#allTests = sorted(["Heart Rate","Glucose","HDL","LDL","Temperature","Diastole","Systole","Triglycerides"])
allTests = {"radio":["Ultrasound","X-Ray","CT Scan","MRI Scan","PET Scan"],"lab":["HDL","LDL","Triglycerides","Glucose"]}


def index(response):
    return render(response,"main/index.html")

def home(response,id):
    p = Patient.objects.get(id = id)
    records = p.record_set.all()[::-1]
    lastRec = p.record_set.last()
    p_attr = p.get_attr()
    return render(response,"main/home.html",{"p_attr":p_attr,"patient":p,"lastRec":lastRec,"records":records})

def newPatient(response):
    if response.method == "POST":
        form = CreatePatient(response.POST) #Retrieves the data submitted in the POST request
        if (form.is_valid()):
            values = form.cleaned_data #Returns a dict. of all the values submitted in the form
            print(values)
            if checkIfUserAvailable(values["name"]):
                new_p = Patient(name = values["name"],age = values["age"],gender = values["gender"],habits = values["habits"],
                blood = values["blood"],medicines = values["medicines"],allergies = values["allergies"],history = values["history"])
                new_p.save()
                return render(response,"main/new_patient.html",{"form":form,"type":"success"})
        return render(response,"main/new_patient.html",{"form":form,"type":"error"})
    else:
        form = CreatePatient()
        #If the method is GET (hence, if we're loading the page rather than submitting the form), we'll only render the HTML.
        return render(response,"main/new_patient.html",{"form":form})

def newRecord(response,id):
    if response.method == "POST":
        p = Patient.objects.get(id = id)
        form = CreateRecord(response.POST)
        print(form.is_valid())
        if (form.is_valid()):
            values = form.cleaned_data
            if values["lab"] == False and values["radiology"] == False: #If no test is required, we will save right away.
                print(values)
                saveRecord(values,p,id)
                return redirect(f"/home/{id}")
            else:
                return render(response,"main/select_tests.html",{"rad":values["radiology"],"lab":values["lab"],
                "labTests":allTests["lab"],"radioTests":allTests["radio"],"vals":values})
    else:
        form = CreateRecord()
        return render(response,"main/new_record.html",{"form":form,"id":id})

def mytestview(request,query):
    print(request.GET['var'])
    return 

def allPatients(response):
    allPatients = Patient.objects.all()[::-1] # Retrieve all the patients (in reverse order)
    allPatients = orderPatients(allPatients) # Sort the patients by their last appointment date
    lastRecords = [getLastRecord(x.id) for x in allPatients]
    allVals = zip(allPatients,lastRecords)
    orderPatients(allPatients)
    return render(response,"main/allPatients.html",{"patients":allVals})


def filterPatients(response,name):
    searched = name.lower().replace("-"," ").replace("_"," ")
    allPatients = Patient.objects.all()[::-1]
    filtered = [x for x in allPatients if searched in x.name.lower()]
    lastRecords = [getLastRecord(x.id) for x in filtered]
    #timeDifferences = [datetime.datetime.now().date() - x.date for x in lastRecords]
    allVals = zip(filtered,lastRecords)
    return render(response,"main/allPatients.html",{"patients":allVals})

def viewRecord(response,id):
    record = Record.objects.get(id = id)
    record_attr = record.get_attr()
    n_lab = len(record.tests["lab"])
    n_radio = len(record.tests["radiology"])
    return render(response,"main/view_record.html",{"rec_id":id,"n_lab":n_lab,"n_radio":n_radio,"tests": record.tests, "attr": record_attr})

def deleteRecord(response,id):
    record = Record.objects.get(id = id)
    patientID = record.patient.id
    record.delete()
    return redirect(f"/home/{patientID}")

def testValues(response,id):
    print("Open test values")

# Create your views here.
