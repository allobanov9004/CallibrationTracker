from django.shortcuts import render, redirect, get_object_or_404
from .forms import CalibrationEventForm
from devices.models import MeasurementDevice
from .decorators import only_metrologist_and_admin
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@only_metrologist_and_admin
def add_calibration_event(request, device_pk):
    device = get_object_or_404(MeasurementDevice, pk=device_pk)

    if request.method == 'POST':
        form = CalibrationEventForm(request.POST, request.FILES)


        if form.is_valid():
            event = form.save(commit=False)
            event.device = device
            event.save()

            if event.next_calibration_date:
                device.next_calibration_date = event.next_calibration_date
                device.save(update_fields=['next_calibration_date'])

            return redirect('device_detail', pk=device.pk)
    else:
        form = CalibrationEventForm(initial={
            'calibration_date': timezone.now().date(),
            'calibration_type': 'verification',
            'calibration_result': 'passed'
        })

    return render(request, 'calibrations/add_calibration.html', {
        'form': form,
        'device': device
    })

@login_required
def calibration_history(request, device_pk):
    device = get_object_or_404(MeasurementDevice, pk=device_pk)
    history = device.calibration_events.all().order_by('-calibration_date')
    return render(request, 'calibrations/history.html', {
        'device': device,
        'history': history
    })






            



# Create your views here.
