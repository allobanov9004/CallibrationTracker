from .models import CalibrationEvent, Organization
from django import forms

class CalibrationEventForm(forms.ModelForm):
    class Meta:
        model = CalibrationEvent
        fields = [
            'calibration_type',
            'calibration_date',
            'next_calibration_date',
            'calibration_result',
            'performed_by',
            'calibration_certificate_number',
            'calibration_certificate_file',
            'notes'
        ]
        widgets = {
            'calibration_date': forms.DateInput(attrs={'type': 'date'}),
            'next_calibration_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['performed_by'].queryset = Organization.objects.all()
            
