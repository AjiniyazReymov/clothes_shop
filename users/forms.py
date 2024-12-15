import re

from django import forms
from django.core.exceptions import ValidationError

from .models import CustomUser

class UserCreateForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=15, required=True, label="Telefon nomeriniz")
    password = forms.CharField(label='Parol', widget=forms.PasswordInput, max_length=128)
    password_2 = forms.CharField(label='Paroldi takrarlan', widget=forms.PasswordInput, max_length=128)
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = "Atiniz"
        self.fields['last_name'].label = "Familiyaniz"

    def clean_password_2(self):
        data = self.cleaned_data
        if data['password'] != data['password_2']:
            raise ValidationError('Paroliniz birdey emes')
        return data['password_2']

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        # Проверяем, что номер состоит только из цифр, пробелов, дефисов, скобок и плюса
        if not re.match(r'^\+?[\d\s\-\(\)]{7,15}$', phone):
            raise forms.ValidationError("Telefon nomer qate terilgen")
        return phone

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_picture']