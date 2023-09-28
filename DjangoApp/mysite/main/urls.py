from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("",views.index,name= "index"),
    path("start/",views.index,name = "startMenu"),
    path("home/<str:id>",views.home,name = "index"),
    path("new_patient/",views.newPatient,name = "newPatient"),
    path("all_patients/",views.allPatients),
    path("new_record/<str:id>",views.newRecord,name = "newRecord"),
    path("view_record/<str:id>",views.viewRecord,name="viewRecord"),
    path("delete_record/<str:id>",views.deleteRecord,name = "deleteRecord"),
    path("test_vals/<int:id>",views.deleteRecord,name = "test_vals"),
    path('my-test/', views.mytestview, name='test-view'),
    path('insert_tests/<str:category>/<str:id>',views.InsertTestResults,name="InserTestResults"),
    path('view_tests/<str:category>/<str:id>',views.viewTestResults,name="viewTests"),
    path('register/',views.register_request,name="register"),
    path('login/',views.login_request,name="login"),
    path('logout/',views.logout_request,name="logout"),
    path('delete_notifications/',views.deleteNotifications,name="deleteNotifications"),
    path('predict_xray/<str:path>/',views.getXRayPrediction,name="xRayPredict")
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)