from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'blog'
urlpatterns=[
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('post/new/', views.post_create, name='post_create'),       # Создание поста
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),  # Редактирование поста
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'), # Удаление поста
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

