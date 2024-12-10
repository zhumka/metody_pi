from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post, Category,Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UserRegistrationForm
def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('blog:index')  # Перенаправить на главную или другую страницу
    else:
        form = UserRegistrationForm()
    return render(request, 'blog/registration.html', {'form': form})


from django.contrib.auth.forms import AuthenticationForm
User=get_user_model()

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('blog:index')  # Перенаправляем на главную после успешного входа
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = AuthenticationForm()  # Пустая форма для GET-запроса

    return render(request, 'blog/login.html', {'form': form})



def user_logout(request):
    logout(request)  # Логаут пользователя
    return redirect(reverse('blog:index'))



def index(request):
    posts = Post.objects.filter(category__isnull=False).order_by('-created_at')[:10]  # Последние 10 постов с категорией
    categories = Category.objects.all()  # Для отображения списка категорий в боковой панели или меню
    return render(request, 'blog/index.html', {'posts': posts, 'categories': categories})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Проверка, если пользователь авторизован, передаем форму для комментария
    if request.user.is_authenticated:
        form = CommentForm()
    else:
        form = None

    # Получаем все комментарии для этого поста
    comments = post.comments.all()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Проверка, что комментарий принадлежит текущему пользователю
    if comment.author != request.user:
        messages.error(request, 'Вы не можете удалить чужой комментарий.')
        return redirect('blog:post_detail', pk=comment.post.id)

    comment.delete()
    messages.success(request, 'Комментарий удалён.')
    return redirect('blog:post_detail', pk=comment.post.id)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category)
    return render(request, 'blog/category_detail.html', {'category': category, 'posts': posts})



@login_required
def profile(request):
    # Получаем все посты и комментарии для текущего пользователя
    user_posts = Post.objects.filter(author=request.user)
    user_comments = Comment.objects.filter(author=request.user)

    context = {
        'user_posts': user_posts,
        'user_comments': user_comments,
    }

    return render(request, 'blog/profile.html', context)



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment
from .forms import CommentForm

# Добавление комментария
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user  # Устанавливаем автора комментария
            comment.post = post  # Привязываем комментарий к посту
            comment.save()
            messages.success(request, 'Комментарий успешно добавлен!')
            return redirect('blog:post_detail', pk=post.id)  # Перенаправляем на страницу поста
        else:
            messages.error(request, 'Ошибка при добавлении комментария.')
    else:
        form = CommentForm()

    return render(request, 'blog/add_comment.html', {'form': form, 'post': post})



# List all posts
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})

# View a single post
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


from django.http import HttpResponseForbidden
from .forms import PostForm
# Create a new post
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

# Edit a post
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

# Delete a post
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return HttpResponseForbidden()
    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


