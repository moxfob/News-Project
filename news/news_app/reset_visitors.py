from django.core.management.base import BaseCommand
from django.core.cache import cache

class Command(BaseCommand):
    help = 'Сбросить счетчик посетителей на сегодня'
    
    def handle(self, *args, **options):
        cache.set('today_visitors', 0, 60*60*24)
        self.stdout.write(self.style.SUCCESS('Счетчик посетителей сброшен на 0'))