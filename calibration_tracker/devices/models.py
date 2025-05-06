from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from devices.constants import MEASURE_TYPE, STATUS, STATUS_LABEL_CLASS, STATUS_DISPLAY


class Department(models.Model):
    name = models.CharField('Наименование', max_length=255)
    description = models.TextField('Описание', null=True, blank=True)

    def __str__(self):
        return self.name


class MeasurementDevice(models.Model):
    MEASURE_TYPE = MEASURE_TYPE
    STATUS = STATUS

    name = models.CharField('Наименование', max_length=255)
    device_type = models.CharField('Тип средства измерения', max_length=255)
    serial_number = models.CharField('Заводской номер', max_length=255)
    measure_type = models.CharField('Вид измерений', max_length=255, choices=MEASURE_TYPE)
    measure_range = models.CharField('Диапазон измерений', max_length=255, null=True, blank=True)
    measurement_unit = models.CharField('Единица измерения', max_length=255, null=True, blank=True)
    accuracy_class = models.CharField('Класс точности', max_length=255, null=True, blank=True)
    manufacturer = models.CharField('Производитель', max_length=255, null=True, blank=True)

    owner_department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Подразделение')
    location = models.CharField('Местоположение', max_length=255, null=True, blank=True)
    responsible_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Ответственный')

    last_calibration_date = models.DateField('Дата поверки', null=True, blank=True)
    next_calibration_date = models.DateField('Дата следующей поверки', null=True, blank=True)
    calibration_interval = models.IntegerField('Периодичность поверки', null=True, blank=True)
    status = models.CharField('Статус', max_length=255, choices=STATUS, default='active')

    certificate_number = models.CharField('Номер свидетельства', max_length=255, null=True, blank=True)
    certificate_file = models.FileField('Свидетельство', upload_to='certificates/', null=True, blank=True)
    notes = models.TextField('Примечание', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.serial_number}"

    def get_status(self):
        if not self.next_calibration_date:
            return 'storage'
        if self.next_calibration_date > timezone.now().date():
            return 'valid'
        else:
            return 'overdue'

    def get_status_display(self):
        status = self.get_status()
        return STATUS_DISPLAY[status]

    def get_status_label_class(self):
        return STATUS_LABEL_CLASS[self.get_status()]

    def get_calibration_interval(self):
        if self.calibration_interval:
            return f"{self.calibration_interval} месяцев"
        return 'Не указано'

    def save(self, *args, **kwargs):
        # Если указана дата последней поверки и интервал, вычисляем дату следующей поверки
        if self.last_calibration_date and self.calibration_interval:
            # Добавляем количество месяцев к дате последней поверки
            self.next_calibration_date = self.last_calibration_date + relativedelta(months=self.calibration_interval)
        super().save(*args, **kwargs)

    
    
