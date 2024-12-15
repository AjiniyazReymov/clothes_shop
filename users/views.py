from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from products.models import PageView
from users.forms import UserCreateForm, UserLoginForm, UserUpdateForm


class RegisterView(View):
    def get(self, request):
        create_form = UserCreateForm()
        context = {
            'form': create_form
        }
        return render(request, 'users/register.html', context)

    def post(self, request):
        create_form = UserCreateForm(data=request.POST)
        if create_form.is_valid():
            create_form.save()
            return redirect('users:login')
        else:
            context = {
                'form': create_form
            }
            return render(request, 'users/register.html', context)


class LoginView(View):
    def get(self, request):
        login_form = UserLoginForm()
        return render(request, 'users/login.html', {'login_form': login_form})

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, "You have successfully Logged in")
            return redirect('index')
        else:
            return render(request, 'users/login.html', {'login_form': login_form})


class ProfileView(View):
    def get(self, request):
        return render(request, 'users/profile.html', {'user': request.user})


# class LogoutView(LoginRequiredMixin, View):
#     def get(self, request):
#         logout(request)
#         messages.info(request, 'You seccessfully logget out')
#         return redirect('index')


def logout_view(request):
    # Завершение всех записей в PageView для текущей сессии
    session_key = request.session.session_key
    if session_key:
        # Найти все записи, связанные с текущей сессией
        pageviews = PageView.objects.filter(session_id=session_key)
        for pageview in pageviews:
            # Завершение или обновление статуса записи
            pageview.is_completed = True  # Например, отметка завершения
            pageview.save()

    # Выполнить logout пользователя
    logout(request)
    return redirect('index')  # Перенаправить пользователя на главную страницу

class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        user_update_form = UserUpdateForm(instance=request.user)
        return render(request, 'users/profile_edit.html', {'form': user_update_form})

    def post(self, request):
        user_update_form = UserUpdateForm(
            instance=request.user,
            data=request.POST,
            files=request.FILES
        )
        if user_update_form.is_valid():
            user_update_form.save()
            messages.success(request, 'You successfully updated your profile.')
            return redirect('users:profile')
        return render(request, 'users/profile_edit.html', {'form': user_update_form})