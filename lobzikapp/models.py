from django.db import models
from datetime import date  # для работы с датами в методе get_age
from django.utils.text import slugify  # для преобразования строки в slug-формат (URL-безопасный)
from transliterate import translit  # для транслитерации русского текста в латиницу


class Country(models.Model):
    name = models.CharField(max_length=100)  # Название страны
    slug = models.SlugField(max_length=255, blank=True, unique=False, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            # Транслитерация имени с русского на английский
            translit_name = translit(self.name, 'ru', reversed=True)
            # Приведение к нижнему регистру и замена пробелов на дефисы
            base_slug = slugify(translit_name)

            # Проверка уникальности slug (если нужно, можно убрать unique=False и сделать slug уникальным)
            slug = base_slug
            n = 1
            while Country.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{n}"
                n += 1

            self.slug = slug

        super().save(*args, **kwargs)


class Category(models.Model):
    title = models.CharField(max_length=100)  # Название категории
    slug = models.SlugField(max_length=255, blank=True, unique=False, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            # Транслитерация названия с русского на английский
            translit_title = translit(self.title, 'ru', reversed=True)
            # Приведение к нижнему регистру и замена пробелов на дефисы
            base_slug = slugify(translit_title)

            # Проверка уникальности slug
            slug = base_slug
            n = 1
            while Category.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{n}"
                n += 1

            self.slug = slug

        super().save(*args, **kwargs)


class Star(models.Model):
    name = models.CharField(max_length=100)  # Имя звезды
    slug = models.SlugField(max_length=255, db_index=True, verbose_name="URL")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='stars')
    categories = models.ManyToManyField(Category, related_name='stars')
    birth_date = models.DateField()  # Дата рождения
    content = models.TextField()  # Описание звезды
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True, verbose_name="Фотография")
    is_published = models.BooleanField(default=True)  # Флаг публикации
    time_create = models.DateTimeField(auto_now_add=True)  # Дата создания (автоматически)
    time_update = models.DateTimeField(auto_now=True)  # Дата обновления (автоматически)

    def __str__(self):
        return self.name

    def get_age(self):
        """Вычисляет возраст звезды на основе даты рождения."""
        today = date.today()
        age = today.year - self.birth_date.year
        # Если день рождения еще не наступил в этом году, вычитаем один год
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        return age
    def get_age_with_correct_word(self):
        """Возвращает возраст с правильно склоненным словом 'год'."""
        age = self.get_age()
        if age is None:  # На случай, если возраст не удалось вычислить
            return "Возраст неизвестен"

        last_digit = age % 10
        last_two_digits = age % 100

        if 11 <= last_two_digits <= 14:
            return f"{age} лет"
        elif last_digit == 1:
            return f"{age} год"
        elif 2 <= last_digit <= 4:
            return f"{age} года"
        else:
            return f"{age} лет"

    def save(self, *args, **kwargs):
        if not self.slug:
            # Транслитерация имени с русского на английский
            translit_name = translit(self.name, 'ru', reversed=True)
            # Приведение к нижнему регистру и замена пробелов на дефисы
            base_slug = slugify(translit_name)

            # Проверка уникальности slug
            slug = base_slug
            n = 1
            while Star.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{n}"
                n += 1

            self.slug = slug

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Знаменитость'
        verbose_name_plural = 'Знаменитости'
        ordering = ['-time_create']  # Сортировка по убыванию времени создания
        indexes = [
            models.Index(fields=['-time_create']),  # Индекс для повышения производительности
        ]