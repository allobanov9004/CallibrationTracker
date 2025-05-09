from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

def only_metrologist_and_admin(view_func):
    @login_required
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Проверяем, является ли пользователь метрологом или администратором
        if not hasattr(request.user, 'profile'):
            raise PermissionDenied("Профиль пользователя не найден")
        
        profile = request.user.profile
        role = profile.role
        if role not in ['metrologist', 'admin'] and not request.user.is_superuser:
            raise PermissionDenied("У вас нет доступа к этой странице")
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view
