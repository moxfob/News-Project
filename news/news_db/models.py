from django.db import models
from django.utils import timezone

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    short_description = models.CharField(max_length=75, verbose_name="Краткое описание")
    image = models.ImageField(upload_to="news_image/", blank=True, null=True, verbose_name="Изображение")
    published_to = models.DateTimeField(default=timezone.now, verbose_name="Дата публикации")
    updated_to = models.DateTimeField(auto_now_add=True, verbose_name="Отредактировано в ")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-published_to']

class Role(models.Model):
    title = models.CharField(max_length=20, verbose_name="Роль", unique=True)
    description = models.CharField(max_length=100, verbose_name="Описание роли")


    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"