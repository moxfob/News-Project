from django.urls import path
from news_db import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.news, name='news'),
    path('add-news/', views.add_news, name='add_news'),
    path('news-detail/<int:news_id>', views.news_detail, name='news_detail')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)