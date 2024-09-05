from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, UserSettings

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = ['ozon_client_id', 'ozon_api_key', 'wildberries_client_id', 'wildberries_api_key', 'yandex_client_id', 'yandex_api_key']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'inn', 'phone_number']