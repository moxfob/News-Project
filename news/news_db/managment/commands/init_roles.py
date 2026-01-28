from django.core.management.base import BaseCommand
from news_db.models import Role

class Command(BaseCommand):
    help = 'Создание стандартных ролей'
    
    def handle(self, *args, **options):
        roles = [
            ('Администратор', 'Полный доступ к системе'),
            ('Редактор', 'Может добавлять и редактировать новости'),
            ('Пользователь', 'Обычный пользователь'),
        ]
        
        for title, description in roles:
            role, created = Role.objects.get_or_create(
                title=title,
                defaults={'description': description}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Создана роль: {title}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ Роль уже существует: {title}'))