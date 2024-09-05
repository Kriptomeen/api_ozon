from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserSettingsForm, UserProfileForm
from .models import UserSettings

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'authentication/login.html'
    
    def get_success_url(self):
        return reverse_lazy('home')
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().get(request, *args, **kwargs)

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из аккаунта.')
    return redirect('login')

@login_required
def user_settings(request):
    user_settings, created = UserSettings.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        settings_form = UserSettingsForm(request.POST, instance=user_settings)
        profile_form = UserProfileForm(request.POST, instance=request.user)
        if settings_form.is_valid() and profile_form.is_valid():
            settings_form.save()
            profile_form.save()
            messages.success(request, 'Настройки успешно обновлены.')
            return redirect('user_settings')
    else:
        settings_form = UserSettingsForm(instance=user_settings)
        profile_form = UserProfileForm(instance=request.user)
    
    return render(request, 'authentication/user_settings.html', {
        'settings_form': settings_form,
        'profile_form': profile_form
    })