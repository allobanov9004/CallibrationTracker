from django.urls import path
from . import views

app_name = 'calibrations'

urlpatterns = [
    path('<int:device_pk>/add/', views.add_calibration_event, name='add_calibration_event'),
    path('<int:device_pk>/history/', views.calibration_history, name='calibration_history'),
]