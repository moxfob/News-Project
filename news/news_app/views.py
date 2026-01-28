from django.shortcuts import render
from news_db.models import News
from django.utils import timezone
from django.core.cache import cache
from accounts.models import User
from django.contrib import messages
from django.shortcuts import redirect
from .models import Appeal

def index(request):
    latest_news = News.objects.filter(is_active=True, published_to__lte=timezone.now()).order_by('-published_to')[:5]
    
    total_news = News.objects.filter(is_active=True).count()
    
    if not request.session.get('visited_today'):
        visitors = cache.get('today_visitors', 0)
        visitors += 1
        cache.set('today_visitors', visitors, 60*60*24)
        request.session['visited_today'] = True
    
    visitors_today = cache.get('today_visitors', 0)
    
    context = {
        'latest_news': latest_news,
        'total_news': total_news,
        'visitors_today': visitors_today,
    }
    return render(request, "news_app/index.html", context)


def about(request):
    total_news = News.objects.filter(is_active=True).count()
    total_users = User.objects.count()
    visitors_today = cache.get('today_visitors', 0)
    
    context = {
        'total_news': total_news,
        'total_users': total_users,
        'visitors_today': visitors_today,
    }
    return render(request, "news_app/about.html", context)

def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if not name or len(name.strip()) < 2:
            messages.error(request, 'Введите корректное имя')
            return redirect('contacts')
        
        if not email or '@' not in email:
            messages.error(request, 'Введите корректный email')
            return redirect('contacts')
        
        if not message or len(message.strip()) < 10:
            messages.error(request, 'Сообщение должно содержать не менее 10 символов')
            return redirect('contacts')
        
        try:
            appeal = Appeal(
                full_name=name.strip(),
                email=email.strip(),
                theme=subject if subject else 'general',
                message=message.strip(),
                created_at=timezone.now()
            )
            appeal.save()
            
            messages.success(request, '✅ Ваше обращение успешно отправлено! Мы ответим вам в ближайшее время.')
            return redirect('contacts')
            
        except Exception as e:
            messages.error(request, f'❌ Произошла ошибка при отправке. Попробуйте позже.')
            print(f"Appeal save error: {e}")
            return redirect('contacts')
    
    return render(request, "news_app/contacts.html")