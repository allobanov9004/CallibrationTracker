from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from devices.models import Department

class Profile(models.Model):
    ROLE_CHOICES = (
        ('storekeeper', 'Кладовщик'),
        ('metrologist', 'Метролог'),
        ('admin', 'Администратор'),
        ('engineer', 'Инженер'),
        ('worker', 'Работник'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField('Роль', max_length=255, choices=ROLE_CHOICES, default='worker')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Подразделение")
    phone_number = models.CharField('Телефон', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
