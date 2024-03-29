from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


def user_login(request):
    if request.method == 'POST' or None:
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse('Аутентификация прошла успешно')
            else:
                return HttpResponse('Отключенный аккаунт')
        else:
            return HttpResponse('Неверный логин')
    else:
        form = LoginForm()
    context = {
        'form': form,
    }
    return render(request, 'account/login.html', context)


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)  # Создаем нового пользователя, но пока не сохраняем в базу данных.
            new_user.set_password(user_form.cleaned_data['password'])  # Задаем пользователю зашифрованный пароль.
            new_user.save()  # Сохраняем пользователя в базе данных.
            profile = Profile.objects.create(user=new_user)  # Создание профиля пользователя.
            profile.save()  # Сохраняем профиль в базе данных.
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно обновлен')
        else:
            messages.error(request, 'Ошибка при обновлении вашего профиля')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'account/edit.html', context=context)
