from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Category, Comment

class BlogTestCase(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = Client()
        self.client.login(username='testuser', password='password123')

        # Создаем категорию и пост
        self.category = Category.objects.create(name='TestCategory', slug='test-category')
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            author=self.user,
            category=self.category
        )

    def test_index_view(self):
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_post_detail_view(self):
        response = self.client.get(reverse('blog:post_detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is a test post.')

    def test_post_create_view(self):
        response = self.client.post(reverse('blog:post_create'), {
            'title': 'New Test Post',
            'content': 'Content for new post.',
            'category': self.category.pk,
        })
        self.assertEqual(response.status_code, 302)  # Redirect to post detail
        new_post = Post.objects.get(title='New Test Post')
        self.assertEqual(new_post.content, 'Content for new post.')
        self.assertEqual(new_post.author, self.user)

    def test_post_edit_view(self):
        response = self.client.post(reverse('blog:post_edit', kwargs={'pk': self.post.pk}), {
            'title': 'Updated Test Post',
            'content': 'Updated content.',
            'category': self.category.pk,
        })
        self.assertEqual(response.status_code, 302)
        updated_post = Post.objects.get(pk=self.post.pk)
        self.assertEqual(updated_post.title, 'Updated Test Post')
        self.assertEqual(updated_post.content, 'Updated content.')

    def test_post_delete_view(self):
        response = self.client.post(reverse('blog:post_delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_add_comment_view(self):
        response = self.client.post(reverse('blog:add_comment', kwargs={'post_id': self.post.pk}), {
            'content': 'This is a test comment.',
        })
        self.assertEqual(response.status_code, 302)
        comment = Comment.objects.get(post=self.post)
        self.assertEqual(comment.content, 'This is a test comment.')
        self.assertEqual(comment.author, self.user)

    def test_delete_comment_view(self):
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Comment to delete.'
        )
        response = self.client.post(reverse('blog:delete_comment', kwargs={'comment_id': comment.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())

    def test_category_detail_view(self):
        response = self.client.get(reverse('blog:category_detail', kwargs={'slug': self.category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_signup_view(self):
        self.client.logout()
        response = self.client.post(reverse('blog:signup'), {
            'username': 'newuser',
            'password': 'newpassword123',
        })
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        self.client.logout()
        response = self.client.post(reverse('blog:login'), {
            'username': 'testuser',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 302)  # Redirect to index
