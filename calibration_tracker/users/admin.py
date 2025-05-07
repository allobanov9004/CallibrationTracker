from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'department', 'phone_number')
    search_fields = ('user__username', 'role', 'department__name', 'phone_number')
    list_filter = ('role', 'department')
