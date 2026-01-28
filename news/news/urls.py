from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news_app.urls')),
    path('news/', include('news_db.urls')),
    path('profile/', include('accounts.urls'))
]
