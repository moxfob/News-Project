from django.shortcuts import render, get_object_or_404
from .models import News
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from news_db.models import News
from django.contrib import messages
from django.shortcuts import redirect

def news(request):
    latest_news = News.objects.filter(is_active = True, published_to__lte = timezone.now()).order_by('-published_to')
    context = {
        'latest_news': latest_news,
    }

    return render(request, 'news_db/news.html', context)


@login_required
def add_news(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        short_description = request.POST.get('short_description')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        
        if not all([title, short_description, description]):
            messages.error(request, 'Заполните все обязательные поля')
            return redirect('add_news')
        
        try:
            news = News.objects.create(
                title=title,
                short_description=short_description,
                description=description,
                image=image,
                is_active=True,
                published_to=timezone.now()
            )
            messages.success(request, 'Новость успешно добавлена!')
            return redirect('news_detail', news_id=news.id)
        except Exception as e:
            messages.error(request, f'Ошибка при добавлении новости: {str(e)}')
    
    return render(request, 'news_db/add_news.html')

def news_detail(request, news_id):
    news = get_object_or_404(News, id=news_id)
    return render(request, 'news_db/news_detail.html', {'news': news})