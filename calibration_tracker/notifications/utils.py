from devices.utils import get_device_due_for_calibration
from notifications.models import Notification
from django.utils import timezone
from devices.models import MeasurementDevice


def check_calibration_deadlines(days_ahead=14):

    today = timezone.now().date()
    due_date = today + timezone.timedelta(days=days_ahead)
    
    devices = MeasurementDevice.objects.filter(
        next_calibration_date__gte=today,
        next_calibration_date__lt=due_date
    )

    for device in devices:
        if device.responsible_person:
            Notification.objects.get_or_create(
                recipient=device.responsible_person,
                title=f"Срок поверки {device.name} подходит к концу",
                message=f"Средство измерений {device.name} № {device.serial_number} требует проведения поверки {device.next_calibration_date}",
                related_device=device,
            )

            
