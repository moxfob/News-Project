from django.urls import path
from accounts import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('user/<int:user_id>/', views.profile_view, name='profile'),
    path('user/me/', views.my_profile, name='my_profile'),
    path('login/', views.login, name='login'),
    path('register/', views.registration, name='registration'),
    path('logout/', views.logout_view, name='logout'),
    path('add-email/', views.add_email, name='add_email'),
    path('change-email/', views.edit_email, name='change_email'),
    path('register/', views.registration, name='register'),
    path('admin_actions/', views.admin_actions, name='admin_actions'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)