from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile
from django.contrib.auth.forms import UserCreationForm

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'avatar': 'Загрузить новую аватарку'
        }

class UsernameUpdateForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Новое имя пользователя'
        }),
        label='Новое имя пользователя'
    )
    
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите текущий пароль'
        }),
        label='Текущий пароль',
        required=True
    )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user and 'username' in self.initial:
            self.initial['username'] = self.user.username
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if not username:
            raise ValidationError('Имя пользователя не может быть пустым.')
        
        if len(username) < 3:
            raise ValidationError('Имя пользователя должно содержать минимум 3 символа.')
        
        if len(username) > 30:
            raise ValidationError('Имя пользователя не может превышать 30 символов.')
        
        if User.objects.filter(username=username).exclude(pk=self.user.pk).exists():
            raise ValidationError('Это имя пользователя уже занято.')
        
        import re
        if not re.match(r'^[\w.@+-]+$', username):
            raise ValidationError('Имя пользователя может содержать только буквы, цифры и символы @/./+/-/_')
        
        return username
    
    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise ValidationError('Неверный текущий пароль.')
        return current_password
    
    def save(self):
        self.user.username = self.cleaned_data['username']
        self.user.save()
        return self.user
    
class EmailUpdateForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email'
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(id=self.user.id).exists():
            raise ValidationError('Этот Email уже используется другим пользователем')
        return email
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

class ChangeEmailForms(forms.Form):
    current_email = forms.EmailField(
        label='Текущий Email',
        required = False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Текущий email',
            'readonly': 'readonly'
        })
    )

    new_email = forms.EmailField(
        label='Новый Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите новый email',
            'autocomplete': 'email'
        })
    )

    confirm_email = forms.EmailField(
        label='Подтвердите новый Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтвердите новый email',
            'autocomplete': 'email'
        })
    )

    password = forms.CharField(
        label='Пароль для подтверждения',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user and self.user.email:
            self.fields['current_email'].initial = self.user.email

    def clean(self):
        cleaned_data = super().clean()
        new_email = cleaned_data.get('new_email')
        confirm_email = cleaned_data.get('confirm_email')
        password = cleaned_data.get('password')

        if new_email and confirm_email and new_email != confirm_email:
            raise forms.ValidationError('Email адреса не совпадают')
        
        if self.user and password:
            if not self.user.check_password(password):
                raise forms.ValidationError('Неверный пароль')
            
        if new_email and User.objects.filter(email=new_email).exclude(id=self.user.id).exists():
            raise forms.ValidationError('Этот email уже используется')
        
        return cleaned_data
    
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email (Необязатель)'
        }),
        label="Email"
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Придумайте имя пользователя'
        }),
        label='Имя пользователя',
        help_text='Только буквы, цифры и @/./+/-/_'
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Придумайте пароль'
        }),
        label='Пароль',
        help_text='Пароль должен содержать не менее 8 символов'
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        }),
        label='Подтверждение пароля'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким именем пользователя уже существует')
        return username