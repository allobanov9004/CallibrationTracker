from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from notifications.utils import check_calibration_deadlines

@receiver(user_logged_in)
def on_user_login(sender, request, user, **kwargs):
    print("Сигнал user_logged_in сработал!")
    check_calibration_deadlines(days_ahead=14)
