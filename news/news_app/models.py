from django.db import models
from django.utils import timezone

class Appeal(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('in_progress', 'В обработке'),
        ('resolved', 'Решено'),
        ('closed', 'Закрыто'),
    ]
    
    THEME_CHOICES = [
        ('general', 'Общий вопрос'),
        ('editorial', 'Редакция'),
        ('advertising', 'Реклама'),
        ('support', 'Техподдержка'),
        ('cooperation', 'Сотрудничество'),
        ('other', 'Другое'),
    ]

    full_name = models.CharField(
        max_length=100, 
        verbose_name="ФИО обращавшегося"
    )
    email = models.EmailField(
        verbose_name="Электронная почта"
    )
    theme = models.CharField(
        max_length=50,
        choices=THEME_CHOICES,
        default='general',
        verbose_name="Тема обращения"
    )
    custom_theme = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Своя тема (если выбрано 'Другое')"
    )
    message = models.TextField(
        verbose_name="Сообщение"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Статус обращения"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )
    admin_notes = models.TextField(
        blank=True,
        verbose_name="Заметки администратора"
    )
    
    def __str__(self):
        return f"Обращение от {self.full_name} ({self.get_theme_display()})"
    
    class Meta:
        verbose_name = "Обращение"
        verbose_name_plural = "Обращения"
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if self.pk:
            old_status = Appeal.objects.get(pk=self.pk).status
            if old_status != self.status:
                self.updated_at = timezone.now()
        super().save(*args, **kwargs)
    
    def get_display_theme(self):
        if self.theme == 'other' and self.custom_theme:
            return self.custom_theme
        return self.get_theme_display()