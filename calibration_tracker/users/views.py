from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from devices.models import Department
from .models import Profile
from .forms import SignUpForm, ProfileForm

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user
        if not Profile.objects.filter(user=user).exists():
            Profile.objects.create(user=user)
        
        # Если пользователь пытается войти в админку
        if 'next' in self.request.GET and self.request.GET['next'].startswith('/admin/'):
            if not user.is_staff:
                messages.error(self.request, 'У вас нет прав для доступа к админке.')
                return redirect('users:login')
        
        return response



@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.profile.phone_number = form.cleaned_data['phone']
            user.save()

            profile = user.profile
            profile.department = form.cleaned_data['department']
            profile.save()

            messages.success(request, 'Профиль успешно обновлен.')
            return redirect('users:profile')
    else:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'phone': request.user.profile.phone_number,
            'department': request.user.profile.department if hasattr(
                request.user, 'profile'
            ) else None
        }
        form = ProfileForm(initial=initial_data)

    departments = Department.objects.all()
    return render(
        request,
        'users/profile.html',
        {'form': form, 'departments': departments}
    )

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешно завершена.')
            return redirect('device_list')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def has_edit_permission(user, device):
    if not user.is_authenticated:
        return False

    return (
        user == device.responsible_person or
        (hasattr(user, 'profile') and user.profile and user.profile.role in ['metrologist', 'admin']) or
        user.is_superuser
    )
