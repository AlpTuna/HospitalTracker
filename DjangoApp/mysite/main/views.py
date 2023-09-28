import json
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth import login,authenticate,logout
from .models import Patient,Record,User,Notification,DailyPatients
from .forms import CreatePatient,CreateRecord,RegistrationForm,LoginForm
import datetime
from .encryption_util import encrypt,decrypt
from .scripts import register,checkIfUserAvailable,getLastRecord,saveRecord,orderPatients,CreateInsertTestForm,UpdateTests,login_script, GetPrediction

# allTests is an array that stores all types of tests in arrays. In each array the first element is the name of the test and
# second element is the type of value it gets.
allTests = {"radiology":{"Ultrasound":"file","X-Ray":"file","CT":"file","MRI":"file","PET":"file"},
            "lab":{"HDL":"int","LDL":"int","Triglycerides":"int","Glucose":"int"}}

labTests = list(allTests["lab"].keys()) # All lab tests in array (without their value type)
radioTests = list(allTests["radiology"].keys()) # All radiology tests in array (without their value type)

def index(response):
    if response.user.is_authenticated:
        ref_count = len(Record.objects.filter(ref_dr_id = response.user.id))
        notifs = Notification.objects.filter(user = response.user.id)
        todays_record = DailyPatients.objects.filter(day = datetime.datetime.today(),doctor=response.user).first()
        last_records = DailyPatients.objects.filter(doctor=response.user)[::]
        print(last_records)
        last_vals = str([x.amount for x in last_records])
        last_vals_titles = str([x.day.strftime("%d %b") for x in last_records])
        if todays_record:
            app_count = todays_record.amount
        else:
            app_count = 0
        return render(response,"main/index.html",{"ref_count":ref_count,"notification_count":len(notifs),
        "notifications":notifs,"notif_ids":[x.id for x in notifs],"apps_today":app_count,
        "last_vals":last_vals,"last_days":last_vals_titles})
    return render(response,"main/landing_page.html")

def getXRayPrediction(request,path):
    print(GetPrediction(path))
    return HttpResponse(GetPrediction(path))

def home(response,id):
    decrypted_id = decrypt(id)
    p = Patient.objects.get(id = decrypted_id)
    records = p.record_set.all()[::-1]
    p_attr = p.get_attr()
    p_id_enc = encrypt(decrypted_id) #I'm creating a diferent encryption for different operations
    records_attr = []
    for record in records:
        records_attr.append({"enc_id":encrypt(record.id),"date":record.date,"reason":record.reason,
        "doctor":User.objects.get(id = record.doctor_id)})
    return render(response,"main/home.html",{"p_attr":p_attr,"patient":p,"records":records_attr,"p_id_enc":p_id_enc})

def register_request(response):
    if response.method == "POST":
        print(response.POST)
        form = RegistrationForm(response.POST)
        if form.is_valid():
            values = form.cleaned_data
            print(values)
            if(register(values) == 0):
                print("Registration unsuccessfull")
        return redirect("/")
    else:
        form = RegistrationForm()
        return render(response,"main/register.html",{"form":form})

def login_request(response):
    if response.method == "POST":
        form = LoginForm(response.POST)
        if form.is_valid():
            values = form.cleaned_data
            print(values)
            user = authenticate(response,username=values["name"], password=values["password"])
            #login_attempt = login_script(values)
            #if login_attempt in (1,2): # Login is unsuccessfull
            #    return render(response,"main/login.html",{"form":LoginForm(),"result":login_attempt})
            #else:
            if user is None:
                print("Login Unsuccessful")
                return render(response,"main/login.html",{"form":LoginForm(),"result":1})
            else:
                login(response,user)
                print(response.user)
                print("Correct", response.user.is_authenticated)
                return redirect("/all_patients/")
        else:
            return redirect("/")
    else:
        form = LoginForm()
        return render(response,"main/login.html",{"form":form,"result":0})

def logout_request(response):
    logout(response)
    return redirect("/")

def newPatient(response):
    if response.user.is_authenticated == False:
        return redirect("/")
    if response.method == "POST":
        form = CreatePatient(response.POST) #Retrieves the data submitted in the POST request
        if (form.is_valid()):
            values = form.cleaned_data #Returns a dict. of all the values submitted in the form
            print(values)
            if checkIfUserAvailable(values["name"]):
                new_p = Patient.objects.create(name = values["name"],birthday = values["birthday"],gender = values["gender"],habits = values["habits"],
                blood = values["blood"],medicines = values["medicines"],allergies = values["allergies"],history = values["history"])
                new_p.doctors.add(response.user)
                new_p.save()
                return render(response,"main/new_patient.html",{"form":form,"type":"success"})
            else:
                patient = Patient.objects.get(name = values["name"])
                patient.doctors.add(response.user)
                patient.save()
                return render(response,"main/new_patient.html",{"form":form,"type":"sameName"})
        return render(response,"main/new_patient.html",{"form":form,"type":"error"})
    else:
        #If the method is GET (hence, if we're loading the page rather than submitting the form), we'll only render the HTML.
        form = CreatePatient()
        return render(response,"main/new_patient.html",{"form":form})

def newRecord(response,id):
    if response.user.is_authenticated == False:
        return redirect("/")
    if response.method == "POST":
        dec_id = decrypt(id)
        form = CreateRecord(response.POST)
        if (form.is_valid()):
            values = form.cleaned_data
            if values["lab"] == False and values["radiology"] == False: #If no test is required, we will save right away.
                values["radioTests"]= []
                values["labTests"] = []
                print(values)
                saveRecord(values,dec_id,response.user)
                return redirect(f"/home/{encrypt(dec_id)}")
            else:
                return render(response,"main/select_tests.html",{"rad":values["radiology"],"lab":values["lab"],
                "labTests":labTests,"radioTests":radioTests,"id_enc":dec_id,"patient":Patient.objects.get(id = dec_id),
                "vals":json.dumps(values)})
    else:
        form = CreateRecord()
        return render(response,"main/new_record.html",{"form":form,"id":id})

def deleteNotifications(request):
    notifs = request.POST.get("notifications")
    notifs = json.loads(notifs)
    if type(notifs) == list:
        for notif_id in notifs:
            Notification.objects.get(id = notif_id).delete()
    elif type(notifs) == int:
        Notification.objects.get(id = notifs).delete()
    return redirect("/")

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
    saveRecord(allVals,id,response.user)
    for doc in User.objects.filter(specialization = User.Specialization.Laboratory):
        Notification.objects.create(text=f"Dr {response.user.username} requested tests for {Patient.objects.get(id = id).name}",user=doc)
    return redirect(f"/home/{encrypt(id)}")
    
def allPatients(response):
    if response.user.is_authenticated == False:
        print("User is not authenticated",response.user.is_authenticated)
        return redirect("/")
    
    filter_name = response.GET.get("name","")
    allPatients2 = Patient.objects.all()[::-1] # Retrieve all the patients (in reverse order)
    allPatients = []

    for patient in allPatients2:
        if patient.doctors.filter(id=response.user.id).exists() and filter_name.lower() in patient.name.lower():
            allPatients.append(patient)
    if response.user.specialization == User.Specialization.Laboratory:
        allPatients = Patient.objects.all()[::-1]
    i = 0
    all_p = []
    # I could also use a dict but it can become more complex to pass dict to HTML. Therefore, I'm using array instead.
    for p in allPatients:
        last_rec = getLastRecord(p.id)
        all_p.append({"encrypted_id": encrypt(p.id),"name":p.name,"gender":p.gender,"age":datetime.datetime.today().year-p.birthday.year,
                      "reason":"","last_rec_date":""})
        if last_rec != None:#If patient has a record, we're gonna add its values
            all_p[i]["reason"] = last_rec.reason
            all_p[i]["last_rec_date"] = last_rec.date
        i += 1    

    return render(response,"main/allPatients.html",{"patients":all_p,"count":i})

def viewRecord(response,id):
    dec_id = decrypt(id)
    record = Record.objects.get(id = dec_id)
    record_attr = record.get_attr()
    lab_tests = ','.join([x for x in record.tests["lab"] if x != "verified"])
    radio_tests = ','.join([x for x in record.tests["radiology"] if x != "verified"])
    n_lab = len(record.tests["lab"])-1
    n_radio = len(record.tests["radiology"])-1
    print(record_attr)
    is_lab_dr = response.user.specialization == User.Specialization.Laboratory
    return render(response,"main/view_record.html",{"rec_id":id,"n_lab":n_lab,"n_radio":n_radio,"tests": record.tests,
                "radio_tests":radio_tests,
                "lab_tests":lab_tests,
                "attr": record_attr,"lab_verified":record.tests["lab"]["verified"],
                "radio_verified":record.tests["radiology"]["verified"],
                "is_lab_dr":is_lab_dr})

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
        record_updated = Record.objects.get(id = dec_id)
        Notification.objects.create(text = f"Added test results ({category.title()}) for {Patient.objects.get(id = record_updated.patient_id).name} by {response.user.username}.",
        user = User.objects.get(id = record_updated.doctor_id))
        return redirect(f"/view_record/{id}")

def viewTestResults(response,id,category):
    dec_id = decrypt(id)
    record = Record.objects.get(id = dec_id)
    tests = {x:[record.tests[category][x],allTests[category][x]] for x in record.tests[category] if x != "verified"}#Get the tests (in dict.) excluding 'verified'
    for x in tests:
        if tests[x][1] == "file":
            tests[x][0] = json.loads(tests[x][0])[0] #dict containing model, id, fields
    return render(response,"main/view_tests.html",{"tests":tests})

def deleteRecord(response,id):
    dec_id = decrypt(id)
    record = Record.objects.get(id = dec_id)
    patientID = record.patient.id
    record.delete()
    return redirect(f"/home/{encrypt(patientID)}")