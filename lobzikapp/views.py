from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound
from datetime import date, timedelta
from .models import Star, Country, Category
from .forms import StarForm
from django.shortcuts import redirect  # Импортируем redirect
from django.contrib import messages  # Импортируем messages

def index(request):
    """
    Главная страница: выводим все звёзды + выделяем, у кого сегодня/завтра/послезавтра день рождения.
    """
    # Получаем все опубликованные звезды
    all_stars = Star.objects.filter(is_published=True)

    
    # Получаем текущую дату
    today = date.today()
    tomorrow = today + timedelta(days=1)
    day_after_tomorrow = today + timedelta(days=2)
    
    # Находим звезд с днями рождения
    today_stars = []
    tomorrow_stars = []
    day_after_tomorrow_stars = []
    
    for star in all_stars:
        # Проверяем месяц и день (без учета года)
        if star.birth_date.month == today.month and star.birth_date.day == today.day:
            today_stars.append(star)
        elif star.birth_date.month == tomorrow.month and star.birth_date.day == tomorrow.day:
            tomorrow_stars.append(star)
        elif star.birth_date.month == day_after_tomorrow.month and star.birth_date.day == day_after_tomorrow.day:
            day_after_tomorrow_stars.append(star)
    
    # Получаем все страны и категории для меню
    countries = Country.objects.all()
    categories = Category.objects.all()
    
    context = {
        'stars': all_stars,
        'today_stars': today_stars,
        'tomorrow_stars': tomorrow_stars,
        'day_after_tomorrow_stars': day_after_tomorrow_stars,
        'today_date': today,
        'tomorrow_date': tomorrow,
        'day_after_tomorrow_date': day_after_tomorrow,
        'star_countries': countries,
        'star_categories': categories,
        'title': 'Дни рождения звезд'
    }
    return render(request, 'lobzikapp/index.html', context)


def star_detail(request, slug):
    """
    Детальная страница конкретной звезды: /person/<slug>/
    """
    # Получаем объект звезды по slug или выбрасываем 404 ошибку
    star = get_object_or_404(Star, slug=slug, is_published=True)

    # Получаем все страны и категории для меню
    countries = Country.objects.all()
    categories = Category.objects.all()

    context = {
        'star': star,
        'star_countries': countries,
        'star_categories': categories,
    }

    return render(request, 'lobzikapp/lobzikapp_detail.html', context)


def about(request):
    # Подсчет статистики
    stats = {
        'stars': Star.objects.filter(is_published=True).count(),
        'countries': Country.objects.count(),
        'categories': Category.objects.count(),
    }
    
    # Описание сайта (можно вынести в настройки или модель, если нужно)
    description = (
        "Borntoday.ru — это сайт, посвященный дням рождения знаменитостей. "
        "Здесь вы найдете информацию о звездах, их биографии, даты рождения и многое другое."
    )
    
    context = {
        'title': 'О сайте',
        'description': description,
        'stats': stats,
        'star_countries': Country.objects.all(),  # Для боковой панели
        'star_categories': Category.objects.all(),  # Для боковой панели
    }
    return render(request, 'lobzikapp/about.html', context)


def stars_by_country(request, slug):
    country = get_object_or_404(Country, slug=slug)
    filtered_stars = Star.objects.filter(country=country, is_published=True)

    countries = Country.objects.all()
    categories = Category.objects.all()

    context = {
        'stars': filtered_stars,
        'country_name': country.name,
        'star_countries': countries,
        'star_categories': categories,
        'title_template': 'Знаменитости из страны'
    }
    return render(request, 'lobzikapp/country.html', context)


def stars_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    filtered_stars = Star.objects.filter(categories=category, is_published=True)

    countries = Country.objects.all()
    categories = Category.objects.all()

    context = {
        'stars': filtered_stars,
        'category_name': category.title,
        'star_countries': countries,
        'star_categories': categories,
        'title_template': 'Знаменитости из отрасли',
    }
    return render(request, 'lobzikapp/industry.html', context)

def add_star(request):
    """
    Представление для добавления новой знаменитости
    """
    if request.method == 'POST':
        form = StarForm(request.POST, request.FILES)
        if form.is_valid():
            star = form.save(commit=False)
            star.is_published = True
            star.save()
            form.save_m2m()  # Сохраняем связи many-to-many
            messages.success(request, f'Знаменитость "{star.name}" успешно добавлена!')
            return redirect('star_detail', slug=star.slug)
    else:
        form = StarForm()
    
    # Получаем все страны и категории для меню
    countries = Country.objects.all()
    categories = Category.objects.all()
    
    context = {
        'form': form,
        'title': 'Добавление знаменитости',
        'star_countries': countries,
        'star_categories': categories,
    }
    return render(request, 'lobzikapp/add-star.html', context)

def star_delete(request, pk):
    star = get_object_or_404(Star, pk=pk)
    if request.method == "POST":
        star.delete()
        return redirect('star_index')
    return render(request, 'lobzikapp/star_confirm_delete.html', {'star': star})

def sitemap(request):
    stars = Star.objects.filter(is_published=True).order_by('name')

    RUSSIAN_ALPHABET = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ'

    
    # Список букв, на которые есть знаменитости
    active_letters = set()
    for star in stars:
        first_letter = star.name[0].upper()
        if first_letter in RUSSIAN_ALPHABET:
            active_letters.add(first_letter)
    
    context = {
        'stars': stars,
        'star_countries': Country.objects.all(),
        'star_categories': Category.objects.all(),
        'alphabet': RUSSIAN_ALPHABET,
        'active_letters': active_letters,
    }
    return render(request, 'lobzikapp/sitemap.html', context)

def sitemap_letter(request, letter):

    RUSSIAN_ALPHABET = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ'

    # Приводим букву к верхнему регистру
    letter = letter.upper()
    
    # Фильтруем звезды по первой букве
    stars = Star.objects.filter(
        is_published=True,
        name__istartswith=letter
    ).order_by('name')
    
    # Список букв, на которые есть знаменитости
    all_stars = Star.objects.filter(is_published=True)
    active_letters = set()
    for star in all_stars:
        first_letter = star.name[0].upper()
        if first_letter in RUSSIAN_ALPHABET:
            active_letters.add(first_letter)
    
    context = {
        'stars': stars,
        'star_countries': Country.objects.all(),
        'star_categories': Category.objects.all(),
        'alphabet': RUSSIAN_ALPHABET,
        'active_letters': active_letters,
        'current_letter': letter,
    }
    return render(request, 'lobzikapp/sitemap_letter.html', context)