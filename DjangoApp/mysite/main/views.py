import json
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import Patient,Record
from .forms import CreatePatient,CreateTests,SelectTests,CreateRecord
from .encryption_util import encrypt,decrypt
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
    decrypted_id = decrypt(id)
    p = Patient.objects.get(id = decrypted_id)
    records = p.record_set.all()[::-1]
    p_attr = p.get_attr()
    p_id_enc = encrypt(decrypted_id) #I'm creating a diferent encryption for different operations
    records_attr = []
    for record in records:
        records_attr.append({"enc_id":encrypt(record.id),"date":record.date,"reason":record.reason})
    return render(response,"main/home.html",{"p_attr":p_attr,"patient":p,"records":records_attr,"p_id_enc":p_id_enc})

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
        dec_id = decrypt(id)
        print(dec_id)
        form = CreateRecord(response.POST)
        print(form.is_valid())
        if (form.is_valid()):
            values = form.cleaned_data
            if values["lab"] == False and values["radiology"] == False: #If no test is required, we will save right away.
                print(values)
                saveRecord(values,id)
                return redirect(f"/home/{encrypt(dec_id)}")
            else:
                return render(response,"main/select_tests.html",{"rad":values["radiology"],"lab":values["lab"],
                "labTests":labTests,"radioTests":radioTests,"id_enc":dec_id,"patient":Patient.objects.get(id = dec_id),
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
    print(id)
    saveRecord(allVals,id)
    return redirect(f"/home/{encrypt(id)}")
    
def allPatients(response):
    allPatients = Patient.objects.all()[::-1] # Retrieve all the patients (in reverse order)
    allPatients = orderPatients(allPatients) # Sort the patients by their last appointment date
    all_p = []
    # I could also use a dict but it can become more complex to pass dict to HTML. Therefore, I'm using array instead.
    for index,p in enumerate(allPatients):
        last_rec = getLastRecord(p.id)
        all_p.append({"encrypted_id": encrypt(p.id),"name":p.name,"gender":p.gender,"age":p.age,"reason":"","last_rec_date":""})
        if last_rec != None:#If patient has a record, we're gonna add its values
            all_p[index]["reason"] = last_rec.reason
            all_p[index]["last_rec_date"] = last_rec.date
    return render(response,"main/allPatients.html",{"patients":all_p})


def filterPatients(response,name):
    searched = name.lower().replace("-"," ").replace("_"," ")
    allPatients = Patient.objects.all()[::-1]
    filtered = [x for x in allPatients if searched in x.name.lower()]
    lastRecords = [getLastRecord(x.id) for x in filtered]
    allVals = zip(filtered,lastRecords)
    return render(response,"main/allPatients.html",{"patients":allVals})

def viewRecord(response,id):
    dec_id = decrypt(id)
    record = Record.objects.get(id = dec_id)
    record_attr = record.get_attr()
    lab_tests = ','.join([x for x in record.tests["lab"] if x != "verified"])
    radio_tests = ','.join([x for x in record.tests["radiology"] if x != "verified"])
    n_lab = len(record.tests["lab"])-1
    n_radio = len(record.tests["radiology"])-1
    return render(response,"main/view_record.html",{"rec_id":id,"n_lab":n_lab,"n_radio":n_radio,"tests": record.tests,
                "radio_tests":radio_tests,
                "lab_tests":lab_tests,
                "attr": record_attr,"lab_verified":record.tests["lab"]["verified"],
                "radio_verified":record.tests["radiology"]["verified"]})

def InsertTestResults(response,id,category):
    dec_id = decrypt(id)
    if response.method == "GET":
        record = Record.objects.get(id = dec_id)
        tests = [x for x in record.tests[category] if x != "verified"]
        form = CreateInsertTestForm(tests,allTests[category])
        return render(response,"main/insert_tests.html",{"rec_id":encrypt(dec_id),"type":category,"form":form})
    if response.method == "POST":
        if category == "lab":
            values = response.POST.dict()
            values.pop('csrfmiddlewaretoken')
            values.pop('save-btn') #We dont need the CSRF and the button (name='save-btn') when assigning values
        else:
            values = response.FILES.dict()
            for x in values:
                print(x)
        print(type(values),values)
        UpdateTests(dec_id,category,values)
        return render(response,"main/index.html")

def viewTestResults(response,id,category):
    dec_id = decrypt(id)
    record = Record.objects.get(id = dec_id)
    tests = {x:[record.tests[category][x],allTests[category][x]] for x in record.tests[category] if x != "verified"}#Get the tests (in dict.) excluding 'verified'
    for x in tests:
        if tests[x][1] == "file":
            tests[x][0] = json.loads(tests[x][0])[0] #dict containing model, id, fields
    print(tests)
    return render(response,"main/view_tests.html",{"tests":tests})

def deleteRecord(response,id):
    dec_id = decrypt(id)
    record = Record.objects.get(id = dec_id)
    patientID = record.patient.id
    record.delete()
    return redirect(f"/home/{encrypt(patientID)}")