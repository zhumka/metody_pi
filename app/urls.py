from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views
app_name = 'app'
urlpatterns=[
        path('user/<int:pk>/', views.user_profile, name='user_profile'),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
