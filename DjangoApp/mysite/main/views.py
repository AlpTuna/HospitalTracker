import json
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import Patient,Record
from .forms import CreatePatient,CreateTests,SelectTests,CreateRecord
from .scripts import checkIfUserAvailable,getLastRecord,saveRecord,orderPatients,CreateInsertTestForm,UpdateTests

# allTests is an array that stores all types of tests in arrays. In each array the first element is the name of the test and
# second element is the type of value it gets.
allTests = {"radiology":{"Ultrasound":"file","X-Ray":"file","CT":"file","MRI":"file","PET":"file"},
            "lab":{"HDL":"int","LDL":"int","Triglycerides":"int","Glucose":"int"}}

labTests = list(allTests["lab"].keys()) # All lab tests in array (without their value type)
radioTests = list(allTests["radiology"].keys()) # All radiology tests in array (without their value type)

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
        form = CreateRecord(response.POST)
        print(form.is_valid())
        if (form.is_valid()):
            values = form.cleaned_data
            if values["lab"] == False and values["radiology"] == False: #If no test is required, we will save right away.
                print(values)
                saveRecord(values,id)
                return redirect(f"/home/{id}")
            else:
                return render(response,"main/select_tests.html",{"rad":values["radiology"],"lab":values["lab"],
                "labTests":labTests,"radioTests":radioTests,"id":id,"patient":Patient.objects.get(id = id),
                "vals":json.dumps(values)})
    else:
        form = CreateRecord()
        return render(response,"main/new_record.html",{"form":form,"id":id})

def mytestview(response):
    tests = response.POST.get("tests")
    tests = json.loads(tests)
    allVals = response.POST.get("values")[1:-1] # All the values in string format
    allVals = json.loads(allVals)
    allVals["radioTests"] = []
    allVals["labTests"] = []
    for test in tests:
        if test in radioTests:
            allVals["radioTests"].append(test)
        elif test in labTests:
            allVals["labTests"].append(test)
        else:
            print("Unknown test!")
    id = response.POST.get("id")
    saveRecord(allVals,id)
    return redirect(f"/home/{id}")
    
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
    allVals = zip(filtered,lastRecords)
    return render(response,"main/allPatients.html",{"patients":allVals})

def viewRecord(response,id):
    record = Record.objects.get(id = id)
    record_attr = record.get_attr()
    n_lab = len(record.tests["lab"])-1 # We have -1 because of the element 'verified' in the dict. 
    n_radio = len(record.tests["radiology"])-1 
    return render(response,"main/view_record.html",{"rec_id":id,"n_lab":n_lab,"n_radio":n_radio,"tests": record.tests,
                "attr": record_attr,"lab_verified":record.tests["lab"]["verified"],
                "radio_verified":record.tests["radiology"]["verified"]})

def InsertTestResults(response,id,type):
    if response.method == "GET":
        print(type)
        record = Record.objects.get(id = id)
        print(record.tests)
        tests = [x for x in record.tests[type] if x != "verified"]
        form = CreateInsertTestForm(tests,allTests[type])
        return render(response,"main/insert_tests.html",{"rec_id":id,"type":type,"form":form})
    if response.method == "POST":
        values = response.POST.dict()
        values.pop('csrfmiddlewaretoken')
        values.pop('save-btn') #We dont need the CSRF and the button (name='save-btn') when assigning values
        print(values)
        UpdateTests(id,type,values)
        return render(response,"main/index.html")

def viewTestResults(response,id,type):
    record = Record.objects.get(id = id)
    tests = {x:record.tests[type][x] for x in record.tests[type] if x != "verified"}#Get the tests (in dict.) excluding 'verified'
    return render(response,"main/view_tests.html",{"tests":tests})

def deleteRecord(response,id):
    record = Record.objects.get(id = id)
    patientID = record.patient.id
    record.delete()
    return redirect(f"/home/{patientID}")