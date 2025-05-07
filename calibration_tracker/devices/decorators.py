from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

def worker_cannot_create(view_func):
    @login_required
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'profile') and request.user.profile.role == 'worker':
            raise PermissionDenied("Не прав для добавления СИ")
        return view_func(request, *args, **kwargs)
    return _wrapped_view