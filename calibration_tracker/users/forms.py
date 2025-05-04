from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from devices.models import Department

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2') 


class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, required=False)
    phone = forms.CharField(max_length=11, required=False)
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=True
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'department')

