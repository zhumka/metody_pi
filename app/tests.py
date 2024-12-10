from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import UserProfile
from django.urls import reverse

class UserProfileTestCase(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.profile = UserProfile.objects.create(
            user=self.user,
            bio='This is a test bio.',
            location='Test Location',
            website='https://example.com'
        )
        self.client = Client()

    def test_user_profile_creation(self):
        # Проверяем, что профиль автоматически связан с пользователем
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.bio, 'This is a test bio.')
        self.assertEqual(self.profile.location, 'Test Location')
        self.assertEqual(self.profile.website, 'https://example.com')

    def test_user_profile_view(self):
        # Проверяем доступность страницы профиля
        response = self.client.get(reverse('app:user_profile', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')  # Имя пользователя
        self.assertContains(response, 'This is a test bio.')  # Биография
        self.assertContains(response, 'Test Location')  # Локация
        self.assertContains(response, 'https://example.com')  # Вебсайт

    def test_user_profile_view_invalid_user(self):
        # Проверяем, что для несуществующего пользователя возвращается 404
        response = self.client.get(reverse('app:user_profile', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)

    def test_update_profile(self):
        # Проверяем обновление данных профиля
        self.profile.bio = 'Updated bio'
        self.profile.location = 'Updated location'
        self.profile.save()
        updated_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(updated_profile.bio, 'Updated bio')
        self.assertEqual(updated_profile.location, 'Updated location')
