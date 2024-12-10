# app/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

def user_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'app/user_profile.html', {'user': user})
