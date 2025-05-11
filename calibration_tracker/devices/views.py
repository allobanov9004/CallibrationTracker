from django.shortcuts import render, get_object_or_404, redirect
from .models import MeasurementDevice
from .forms import MeasurementDeviceForm
from django.contrib.auth.decorators import login_required
from .utils import get_overdue_devices
from datetime import date
from users.views import has_edit_permission
from django.core.exceptions import PermissionDenied
from .forms import MeasurementDeviceForm
from .decorators import worker_cannot_create


@worker_cannot_create
def device_create(request):
    if request.method == 'POST':
        form = MeasurementDeviceForm(request.POST, request.FILES, user=request.user)

        if 'measure_type' in request.POST and 'final_submit' not in request.POST:
            measure_type = request.POST.get('measure_type')
            form._update_measurement_unit_field(measure_type)
            return render(request, 'devices/device_form.html', {'form': form})

        if form.is_valid():
            device = form.save(commit=False)
            try:
                profile = request.user.profile
                if profile.role == 'storekeeper':
                    device.responsible_person = request.user
                    device.owner_department = profile.department
            except profile.DoesNotExist:
                pass
            device.save()
            return redirect('device_detail', pk=device.pk)
    else:
        form = MeasurementDeviceForm(user=request.user)


    return render(request, 'devices/device_form.html', {'form': form})


@login_required
def device_update(request, pk):
    device = get_object_or_404(MeasurementDevice, pk=pk)

    if not has_edit_permission(request.user, device):
        raise PermissionDenied("У вас нет прав редактировать это средство измерения")

    if request.method == 'POST':
        form = MeasurementDeviceForm(
            data=request.POST,
            files=request.FILES,
            instance=device,
            user=request.user
        )

        if 'measure_type' in request.POST and 'final_submit' not in request.POST:
            measure_type = request.POST.get('measure_type')
            form._update_measurement_unit_field(measure_type)
            return render(request, 'devices/device_form.html', {'form': form})


        if form.is_valid():

            form.save()
            return redirect('device_detail', pk=device.pk)

    else:
        form = MeasurementDeviceForm(instance=device, user=request.user)

    return render(request, 'devices/device_form.html', {'form': form})


def device_list(request):
    devices = MeasurementDevice.objects.all()
    for device in devices:
        device.can_edit = has_edit_permission(request.user, device)
    return render(request, 'devices/device_list.html', {'devices': devices})


def device_detail(request, pk):
    device = get_object_or_404(MeasurementDevice, pk=pk)
    can_edit = has_edit_permission(request.user, device)
    return render(request, 'devices/device_detail.html', {
        'device': device,
        'can_edit': can_edit
    })


@login_required
def device_delete(request, pk):
    device = get_object_or_404(MeasurementDevice, pk=pk)

    if not has_edit_permission(request.user, device):
        raise PermissionDenied("У вас нет прав удалять это СИ")

    if request.method == 'POST':
        device.delete()
        return redirect('device_list')
    
    return render(request, 'devices/device_confirm_delete.html', {'device': device})


@login_required
def overdue_device_view(request):
    devices = get_overdue_devices()
    return render(request, 'devices/overdue_list.html', {
        'devices': devices,
        'today': date.today()
    })
            
@login_required
def my_devices_view(request):
    devices = MeasurementDevice.objects.filter(responsible_person=request.user)
    return render(request, 'devices/my_devices.html', {'devices': devices})


def update_measurement_unit(request):
    form = MeasurementDeviceForm(data=request.POST or None)
    measure_type = request.POST.get('measure_type')
    form._update_measurement_unit_field(measure_type)

    return render(request, 'devices/includes/measurement_unit_field.html', {'form': form})

    
