# blog/admin.py
from django.contrib import admin
from .models import Category, Post, Comment, Like

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')  # Отображение на странице списка
    search_fields = ('name',)  # Поля поиска

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'views')  # Отображение на странице списка
    search_fields = ('title', 'author__username', 'category__name')  # Поля поиска
    list_filter = ('category', 'created_at')  # Фильтрация
    readonly_fields = ('views', 'created_at', 'updated_at')  # Поля только для чтения
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'author', 'category', 'views', 'created_at', 'updated_at')
        }),
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')  # Отображение на странице списка
    search_fields = ('author__username', 'post__title', 'content')  # Поля поиска
    list_filter = ('created_at',)  # Фильтрация
    readonly_fields = ('created_at', 'updated_at')  # Поля только для чтения
    fieldsets = (
        (None, {
            'fields': ('post', 'author', 'content', 'created_at', 'updated_at')
        }),
    )

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')  # Отображение на странице списка
    search_fields = ('user__username', 'post__title')  # Поля поиска
    list_filter = ('created_at',)  # Фильтрация
    readonly_fields = ('created_at',)  # Поля только для чтения
    fieldsets = (
        (None, {
            'fields': ('user', 'post', 'created_at')
        }),
    )
