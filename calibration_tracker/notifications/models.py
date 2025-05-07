from django.db import models
from django.contrib.auth import get_user_model
from devices.models import MeasurementDevice

User = get_user_model()

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Получатель', related_name='notifications')
    title = models.CharField('Заголовок', max_length=255)
    message = models.TextField('Сообщение')
    is_read = models.BooleanField('Прочитано', default=False)
    created_at = models.DateTimeField('Дата и время создания', auto_now_add=True)
    related_device = models.ForeignKey(
        MeasurementDevice, 
        on_delete=models.SET_NULL, 
        verbose_name='Связанное устройство', 
        null=True, 
        blank=True
    )

    def __str__(self):
        return f'{self.recipient.username} - {self.title}'

    class Meta:
        ordering = ['-created_at']
