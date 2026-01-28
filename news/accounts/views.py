from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login as auth_login
from django.utils import timezone
from datetime import timedelta
from news_db.models import News
from news_db.models import Role as NewsRole
from .models import Profile
from .forms import ProfileUpdateForm, UsernameUpdateForm, EmailUpdateForm, ChangeEmailForms, CustomUserCreationForm

def profile_view(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    profile = profile_user.profile
    
    avatar_form = None
    username_form = None
    password_form = None
    
    if request.user == profile_user:
        avatar_form = ProfileUpdateForm(instance=profile)
        username_form = UsernameUpdateForm(user=request.user, initial={'username': request.user.username})
        password_form = PasswordChangeForm(request.user)
    
    admin_stats = {}
    all_roles = []
    all_users = []
    
    if request.user.is_superuser and request.user == profile_user:
        admin_stats['total_users'] = User.objects.count()
        admin_stats['total_news'] = News.objects.filter(is_active=True).count()
        admin_stats['total_admins'] = User.objects.filter(is_superuser=True).count()
        admin_stats['total_staff'] = User.objects.filter(is_staff=True).count()
        admin_stats['total_editors'] = User.objects.filter(profile__role__title='Редактор').count()
        admin_stats['total_moderators'] = User.objects.filter(profile__role__title='Модератор').count()
        admin_stats['today_users'] = User.objects.filter(date_joined__date=timezone.now().date()).count()
        admin_stats['week_users'] = User.objects.filter(date_joined__gte=timezone.now()-timedelta(days=7)).count()
        admin_stats['total_active_news'] = News.objects.filter(is_active=True, published_to__lte=timezone.now()).count()
        admin_stats['total_draft_news'] = News.objects.filter(is_active=False).count()
        admin_stats['last_24h_news'] = News.objects.filter(published_to__gte=timezone.now()-timedelta(hours=24)).count()
    
    if request.user.is_superuser:
        all_roles = NewsRole.objects.all()
        all_users = User.objects.all().select_related('profile', 'profile__role').order_by('username')
    
    context = {
        'user': profile_user,
        'profile': profile,
        'avatar_form': avatar_form,
        'username_form': username_form,
        'password_form': password_form,
        'is_own_profile': request.user == profile_user,
        'all_roles': all_roles,
        'all_users': all_users,
        **admin_stats
    }
    
    return render(request, 'accounts/profile.html', context)

@login_required
def my_profile(request):
    profile = request.user.profile
    password_form = None

    if request.method == 'POST':
        if 'update_avatar' in request.POST:
            avatar_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
            if avatar_form.is_valid():
                avatar_form.save()
                messages.success(request, 'Аватар успешно обновлен!')
                return redirect('my_profile')
            
        elif 'update_username' in request.POST:
            username_form = UsernameUpdateForm(request.POST, user=request.user)
            if username_form.is_valid():
                user = request.user
                new_username = username_form.cleaned_data['username']
                user.username = new_username
                user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, f'Имя пользователя успешно обновлено на {new_username}!')
                return redirect('my_profile')
                
        elif 'update_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Пароль успешно изменен!')
                return redirect('my_profile')
            else:
                admin_stats = {}
                all_roles = []
                all_users = []
                
                if request.user.is_superuser:
                    admin_stats['total_users'] = User.objects.count()
                    admin_stats['total_news'] = News.objects.filter(is_active=True).count()
                    admin_stats['total_admins'] = User.objects.filter(is_superuser=True).count()
                    all_roles = NewsRole.objects.all()
                    all_users = User.objects.all().select_related('profile', 'profile__role').order_by('username')
                
                context = {
                    'user': request.user,
                    'profile': profile,
                    'avatar_form': ProfileUpdateForm(instance=profile),
                    'username_form': UsernameUpdateForm(user=request.user, initial={'username': request.user.username}),
                    'password_form': password_form,
                    'is_own_profile': True,
                    'all_roles': all_roles,
                    'all_users': all_users,
                    **admin_stats
                }
                return render(request, 'accounts/profile.html', context)
        
        elif request.user.is_superuser and 'user_action' in request.POST:
            user_action = request.POST.get('user_action')
            target_user_id = request.POST.get('target_user_id')
            
            if target_user_id:
                target_user = get_object_or_404(User, id=target_user_id)
                
                if user_action == 'change_role':
                    new_role_id = request.POST.get('new_role')
                    if new_role_id:
                        try:
                            new_role = NewsRole.objects.get(id=new_role_id)
                            target_user.profile.role = new_role
                            target_user.profile.save()
                            messages.success(request, f'Роль пользователя {target_user.username} изменена на {new_role.title}')
                        except NewsRole.DoesNotExist:
                            messages.error(request, 'Роль не найдена')
                
                elif user_action == 'reset_password':
                    new_password = request.POST.get('new_password', User.objects.make_random_password())
                    target_user.set_password(new_password)
                    target_user.save()
                    messages.success(request, f'Пароль пользователя {target_user.username} сброшен. Новый пароль: {new_password}')
                
                elif user_action == 'deactivate':
                    target_user.is_active = not target_user.is_active
                    target_user.save()
                    status = "деактивирован" if not target_user.is_active else "активирован"
                    messages.success(request, f'Пользователь {target_user.username} {status}')
                
                return redirect('my_profile')
    
    else:
        avatar_form = ProfileUpdateForm(instance=profile)
        username_form = UsernameUpdateForm(user=request.user, initial={'username': request.user.username})
        password_form = PasswordChangeForm(request.user)
    
    admin_stats = {}
    all_roles = []
    all_users = []
    
    if request.user.is_superuser:
        admin_stats['total_users'] = User.objects.count()
        admin_stats['total_news'] = News.objects.filter(is_active=True).count()
        admin_stats['total_admins'] = User.objects.filter(is_superuser=True).count()
        admin_stats['total_staff'] = User.objects.filter(is_staff=True).count()
        admin_stats['total_editors'] = User.objects.filter(profile__role__title='Редактор').count()
        admin_stats['total_moderators'] = User.objects.filter(profile__role__title='Модератор').count()
        admin_stats['today_users'] = User.objects.filter(date_joined__date=timezone.now().date()).count()
        admin_stats['week_users'] = User.objects.filter(date_joined__gte=timezone.now()-timedelta(days=7)).count()
        admin_stats['total_active_news'] = News.objects.filter(is_active=True, published_to__lte=timezone.now()).count()
        admin_stats['total_draft_news'] = News.objects.filter(is_active=False).count()
        admin_stats['last_24h_news'] = News.objects.filter(published_to__gte=timezone.now()-timedelta(hours=24)).count()
        all_roles = NewsRole.objects.all()
        all_users = User.objects.all().select_related('profile', 'profile__role').order_by('username')
    
    context = {
        'user': request.user,
        'profile': profile,
        'avatar_form': avatar_form,
        'username_form': username_form,
        'password_form': password_form,
        'is_own_profile': True,
        'all_roles': all_roles,
        'all_users': all_users,
        **admin_stats
    }
    
    return render(request, 'accounts/profile.html', context)

def login(request):
    if request.user.is_authenticated:
        messages.info(request, "Вы уже вошли в аккаунт!")
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Пожалуйста заполните все поля')
            return redirect('login')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Добро пожаловать, {user.username}!")

            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, "Неверное имя пользователя или пароль")
            return redirect('login')
        
    return render(request, 'accounts/login.html')

def registration(request):
    if request.user.is_authenticated:
        messages.info(request, "Вы уже вошли в аккануты!")
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            if form.cleaned_data.get('email'):
                user.email = form.cleaned_data['email']

            user.save()

            profile, created = Profile.objects.get_or_create(user=user)

            try:
                user_role = NewsRole.objects.get(title='Пользователь')
                profile.role = user_role
                profile.save()
            except NewsRole.DoesNotExist:
                user_role = NewsRole.objects.create(
                    title='Пользователь',
                    description='Обычный пользователь системы'
                )

                profile.role = user_role
                profile.save()
                messages.warning(request, 'Роль "Пользователь" была создана автоматически')

            auth_login(request, user)

            messages.success(request, f'Добро пожаловать, {user.username}! Регистрация прошла успешна')
            return redirect('my_profile')
        
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')

    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

@login_required
def logout_view(request):
    auth_logout(request)
    messages.success(request, "Вы успешно вышли из аккаунта!")
    return redirect('home')

@login_required
def add_email(request):
    if request.method == 'POST':
        form = EmailUpdateForm(request.POST, user=request.user)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            messages.success(request, 'Email успешно добавлен')
            return redirect('my_profile')
    else:
        form = EmailUpdateForm(user=request.user)

    return render(request, 'accounts/add_email.html', {'form': form})

@login_required
def edit_email(request):
    if request.method == 'POST':
        form = ChangeEmailForms(request.POST, user=request.user)
        if form.is_valid():
            new_email = form.cleaned_data['new_email']
            request.user.email = new_email
            request.user.save()

            messages.success(request, 'Email успешно изменен!')

            return redirect('my_profile')
        
    else:
        form = ChangeEmailForms(user=request.user)

    return render(request, 'accounts/edit_email.html', {
        'form': form,
        'user': request.user
    })

@login_required
def admin_actions(request):
    if not request.user.is_superuser:
        messages.error(request, "Доступ запрещен!")
        return redirect('home')
    
    if request.method == 'POST':
        user_action = request.POST.get('user_action')
        target_user_id = request.POST.get('target_user_id')
        
        if not target_user_id:
            messages.error(request, "Не указан пользователь!")
            return redirect('my_profile')
        
        target_user = get_object_or_404(User, id=target_user_id)
        
        if user_action == 'change_role':
            new_role_id = request.POST.get('new_role')
            if new_role_id:
                try:
                    new_role = NewsRole.objects.get(id=new_role_id)
                    target_user.profile.role = new_role
                    target_user.profile.save()
                    messages.success(request, f'Роль пользователя {target_user.username} изменена на {new_role.title}')
                except NewsRole.DoesNotExist:
                    messages.error(request, 'Роль не найдена')
        
        elif user_action == 'reset_password':
            new_password = request.POST.get('new_password', User.objects.make_random_password())
            target_user.set_password(new_password)
            target_user.save()
            messages.success(request, f'Пароль пользователя {target_user.username} сброшен. Новый пароль: {new_password}')
        
        elif user_action == 'deactivate':
            target_user.is_active = not target_user.is_active
            target_user.save()
            status = "деактивирован" if not target_user.is_active else "активирован"
            messages.success(request, f'Пользователь {target_user.username} {status}')
        
        return redirect('profile', user_id=target_user_id)
    
    return redirect('my_profile')