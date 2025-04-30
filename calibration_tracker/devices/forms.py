from django import forms
from .models import MeasurementDevice

class MeasurementDeviceForm(forms.ModelForm):
    class Meta:
        model = MeasurementDevice
        fields = [
            'name',
            'device_type',
            'manufacturer',
            'serial_number',
            'location',
            'owner_department',
            'responsible_person',
            'last_calibration_date',
            'next_calibration_date',
            'calibration_interval',
            'certificate_number',
            'status',
            'certificate_file',
            'notes',
        ]
        widgets = {
            'last_calibration_date': forms.DateInput(attrs={'type': 'date'}),
            'next_calibration_date': forms.DateInput(attrs={'type': 'date'}),
        }