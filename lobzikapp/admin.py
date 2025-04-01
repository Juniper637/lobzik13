from django.contrib import admin
from .models import Star, Country, Category

@admin.register(Star)
class StarAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date', 'country', 'is_published', 'time_create')
    list_filter = ('country', 'categories', 'is_published')
    search_fields = ('name', 'content')
    fields = ('name', 'birth_date', 'country', 'categories', 'content', 'photo', 'is_published')  # Без slug
    list_editable = ('is_published',)
    ordering = ('-time_create',)

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}