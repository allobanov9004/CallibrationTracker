from django.shortcuts import render, get_object_or_404, redirect
from .models import MeasurementDevice
from django.db.models import Q
from django.utils import timezone
from .forms import MeasurementDeviceForm
from django.contrib.auth.decorators import login_required



@login_required
def device_create(request):
    if request.method == 'POST':
        form = MeasurementDeviceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('device_list')
    else:
        form = MeasurementDeviceForm()

    return render(request, 'devices/device_form.html', {'form': form})

@login_required
def device_update(request, pk):
    device = get_object_or_404(MeasurementDevice, pk=pk)
    if request.method == 'POST':
        form = MeasurementDeviceForm(request.POST, request.FILES, instance=device)
        if form.is_valid():
            form.save()
            return redirect('device_detail', pk=device.pk)
    else:
        form = MeasurementDeviceForm(instance=device)

    return render(request, 'devices/device_form.html', {
        'form': form,
        'device': device,
    })


def device_list(request):
    query = request.GET.get('q')
    device_type = request.GET.get('device_type')
    owner_department = request.GET.get('owner_department')
    location = request.GET.get('location')
    status = request.GET.get('status')

    devices = MeasurementDevice.objects.all()
    #поиск по заводскому номеру и наименованию
    if query:
        devices = devices.filter(
            Q(name__icontains=query) | 
            Q(serial_number__icontains=query)
        )
    #фильтр по типу средства измерения
    if device_type:
        devices = devices.filter(device_type=device_type)
    #фильтр по владельцу
    if owner_department:
        devices = devices.filter(owner_department=owner_department)
    #фильтр по местоположению
    if location:
        devices = devices.filter(location=location)
    #фильтр по статусу
    if status == 'overdue':
        devices = devices.filter(next_calibration_date__lt=timezone.now().date())
    elif status == 'valid':
        devices = devices.filter(next_calibration_date__gte=timezone.now().date())
    
    
    return render(request, 'devices/device_list.html', {
        'devices': devices,
        'query': query or '',
        'device_type': device_type or '',
        'location': location or '',
        'status': status or '',
        })

def device_detail(request, pk):
    device = get_object_or_404(MeasurementDevice, pk=pk)
    return render(request, 'devices/device_detail.html', {'device': device})

@login_required
def device_delete(request, pk):
    device = get_object_or_404(MeasurementDevice, pk=pk)

    if request.method == 'POST':
        device.delete()
        return redirect('device_list')
    
    return render(request, 'devices/device_confirm_delete.html', {'device': device})
