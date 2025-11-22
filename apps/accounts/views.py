from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm
from .models import AppUser
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin

def login_view(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            usuario = authenticate(request, username=username, password=password)
            if usuario is not None:
                login(request, usuario)
                # Redirigir a la página de bienvenida (perfil)
                return redirect('perfil')
            else:
                form.add_error(None, 'Credenciales inválidas')
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('main_index')

class UserListView(LoginRequiredMixin, ListView):
    login_url = 'accounts:login'
    model = AppUser
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'

class RegisterUserView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})
    
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password1']
                
                # Crear usuario con AbstractUser
                user = AppUser.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name='',
                    last_name=''
                )
                
                # Loguear automáticamente después del registro
                login(request, user)
                return redirect('perfil')
            except Exception as e:
                form.add_error(None, f'Error al crear usuario: {str(e)}')
        
        return render(request, 'accounts/register.html', {'form': form})

