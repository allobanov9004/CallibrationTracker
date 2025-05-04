from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def notifications_list(request):
    notifications = request.user.notifications.all()
    unread_count = notifications.filter(is_read=False).count()
    return render(request, 'notifications/list.html', {'notifications': notifications, 'unread_count': unread_count})

