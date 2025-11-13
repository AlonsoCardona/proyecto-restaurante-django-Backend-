from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario',
                max_length=150, required=True, 
                widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True)
    remember_me = forms.BooleanField(
        label='Recordar mis datos', 
        required=False, initial=False, 
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Usuario',
                max_length=150, required=True, 
                widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Correo electrónico',
                required=True,
                widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True)
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True)
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        
        return cleaned_data

