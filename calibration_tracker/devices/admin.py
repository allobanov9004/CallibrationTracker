from django.contrib import admin
from .models import MeasurementDevice, Department


@admin.register(MeasurementDevice)
class MeasurementDeviceAdmin(admin.ModelAdmin):
    list_display = ('name',
        'device_type',
        'serial_number',
        'last_calibration_date',
        'next_calibration_date'
    )
    search_fields = ('name','device_type', 'serial_number', 'owner_department', 'last_calibration_date', 'next_calibration_date')
    list_filter = ('device_type', 'owner_department', 'last_calibration_date', 'next_calibration_date')
    date_hierarchy = 'next_calibration_date'


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    list_filter = ('name', 'description')


