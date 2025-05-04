from django.utils import timezone
from datetime import timedelta
from devices.models import MeasurementDevice


def get_device_due_for_calibration(days_ahead=14):
    today = timezone.now().date()
    due_date = today + timedelta(days=days_ahead)
    return MeasurementDevice.objects.filter(
        next_calibration_date=due_date
    )

def get_overdue_devices():
    today = timezone.now().date()
    return MeasurementDevice.objects.filter(
        next_calibration_date__lt=today
    )
