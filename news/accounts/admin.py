# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from .models import Profile, Role

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профиль'
    fk_name = 'user'
    fields = ('avatar', 'avatar_preview', 'role')
    readonly_fields = ('avatar_preview',)
    
    def avatar_preview(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" style="width: 100px; height: 100px; object-fit: cover;" />')
        return "Нет аватарки"
    avatar_preview.short_description = 'Превью'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'avatar_preview', 'get_role')
    list_select_related = ('profile',)
    
    def avatar_preview(self, obj):
        if hasattr(obj, 'profile') and obj.profile.avatar:
            return mark_safe(f'<img src="{obj.profile.avatar.url}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;" />')
        return "Нет"
    avatar_preview.short_description = 'Аватар'
    
    def get_role(self, obj):
        if hasattr(obj, 'profile') and obj.profile.role:
            return obj.profile.role.title
        return "Не назначена"
    get_role.short_description = 'Роль'
    get_role.admin_order_field = 'profile__role__title'
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class RoleAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description')