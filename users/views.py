from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView
from .models import CustomUser

from .forms import CustomUserCreationForm
from django.views.generic.edit import CreateView
from dotenv import load_dotenv
import os


class CustomLoginView(LoginView):
    template_name = 'login.html'


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('mailing:home')


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('mailing:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        # self.send_welcome_email(user.email)
        return super().form_valid(form)

    @staticmethod
    def send_welcome_email(user_email):
        subject = 'Добро пожаловать в наш сервис'
        message = 'Спасибо, что зарегистрировались в нашем сервисе!'
        from_email = os.getenv('EMAIL_HOST_USER')
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)


class UserDetailView(DetailView):
    model = CustomUser
    template_name = 'users/user_info.html'
    context_object_name = 'user'

    def get(self, request, pk):
        user_info = get_object_or_404(CustomUser, id=pk)
        if user_info.id == request.user.id:
            user_info_path = reverse_lazy('users:user_info')
            return render(request, 'users/user_info.html', {'user': user_info})
        return HttpResponseForbidden('Войдите в аккаунт для просмотра данных')
