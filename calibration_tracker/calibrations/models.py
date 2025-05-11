from django.db import models
from devices.models import MeasurementDevice
from django.conf import settings
from django.utils import timezone

class Organization(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    

class CalibrationEvent(models.Model):
    TYPE_CHOICES = [
        ('verification', 'Поверка'),
        ('calibration', 'Калибровка'),
        ('control', 'Контроль'),
    ]

    RESULT_CHOICES = [
        ('passed', 'Годен'),
        ('failed', 'Не годен'),
    ]

    device = models.ForeignKey(
        MeasurementDevice,
        on_delete=models.CASCADE,
        related_name='calibration_events'
    )

    calibration_type = models.CharField("Вид работы", max_length=25, choices=TYPE_CHOICES)

    calibration_date = models.DateField("Дата поверки", default=timezone.now)
    next_calibration_date = models.DateField("Дата следующей поверки", blank=True, null=True)

    calibration_result = models.CharField(max_length=255, choices=RESULT_CHOICES, default='passed')

    performed_by = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='calibration_events', verbose_name="Организация")

    calibration_certificate_number = models.CharField("Номер свидетельства", max_length=35, blank=True, null=True)
    calibration_certificate_file = models.FileField(upload_to='calibration_certificates/', blank=True, null=True)

    notes = models.TextField("Примечание", blank=True, null=True) 
    
    def __str__(self):
        return f"{self.calibration_type}: {self.device.name} № {self.device.serial_number} от {self.calibration_date}"
    
    class Meta:
        verbose_name = "Проведение поверки/калибровки"
        verbose_name_plural = "Проведения поверки/калибровки"
        ordering = ['-calibration_date']
