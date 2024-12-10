# app/admin.py
from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'birth_date')  # Отображение на странице списка
    search_fields = ('user__username', 'location')  # Поля поиска
    list_filter = ('location',)  # Фильтрация
    readonly_fields = ('user',)  # Поля только для чтения
    fieldsets = (
        (None, {
            'fields': ('user', 'bio', 'profile_image', 'website', 'location', 'birth_date')
        }),
    )
