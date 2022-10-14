from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name= "index"),
    path("start/",views.index,name = "startMenu"),
    path("home/<int:id>",views.home,name = "index"),
    path("new_patient/",views.newPatient,name = "newPatient"),
    path("all_patients/",views.allPatients),
    path("search=<str:name>",views.filterPatients),
    path("new_record/<int:id>",views.newRecord,name = "newRecord"),
    path("view_record/<int:id>",views.viewRecord,name="viewRecord"),
    path("delete_record/<int:id>",views.deleteRecord,name = "deleteRecord"),
    path("test_vals/<int:id>",views.deleteRecord,name = "test_vals"),
    path('my-test/', views.mytestview, name='test-view'),
    path('insert_tests/<str:type>/<int:id>',views.InsertTestResults,name="InserTestResults"),
    path('view_tests/<str:type>/<int:id>',views.viewTestResults,name="viewTests")
]