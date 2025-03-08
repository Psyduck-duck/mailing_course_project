import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView

from config.settings import EMAIL_HOST_USER
from mailing.models import SendAttempt
from .models import CustomUser
# from mailing.services import CustomUserService

from .forms import CustomUserCreationForm, UserUpdateForm
from django.views.generic.edit import CreateView, UpdateView
from users.models import CustomUser as User


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
        user.is_active = False
        user.token = secrets.token_hex(16)
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{user.token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Перейдите по ссылке, чтобы подтвердить почту: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[
                user.email,
            ],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


@method_decorator(cache_page(60*5), name='dispatch')
class UserDetailView(DetailView):
    model = User
    template_name = 'users/user_info.html'
    context_object_name = 'user'

    def get(self, request, pk):
        user_info = get_object_or_404(CustomUser, id=pk)
        user_id = request.user
        success_attempts_count = SendAttempt.objects.filter(status='Успешно', owner_id=user_id).count()
        unsuccess_attempts_count = SendAttempt.objects.filter(status='Не успешно', owner_id=user_id).count()
        if user_info.id == request.user.id:
            return render(request, 'users/user_info.html',
                          {'user': user_info, 'success_attempts_count': success_attempts_count,
                           'unsuccess_attempts_count': unsuccess_attempts_count})
        return HttpResponseForbidden('Войдите в аккаунт для просмотра данных')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'

    def get_success_url(self):
        return reverse_lazy("users:user_info", kwargs={'pk': self.object.id})


class BlockUserView(LoginRequiredMixin, View):
    model = User
    template_name = 'users/user_block_confirm.html'
    success_url = reverse_lazy('mailing:home')
    login_url = reverse_lazy('users:login')
    context_object_name = 'user'

    def get(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)
        if not request.user.has_perm('users.can_block_user'):
            return HttpResponseForbidden('У вас нет прав для блокировки / разблокировки пользователя')
        return render(request, 'users/user_block_confirm.html', {'user': user})

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)
        if not request.user.has_perm('users.can_block_user'):
            return HttpResponseForbidden('У вас нет прав для блокировки / разблокировки пользователя')
        if not user.is_blocked:
            user.is_blocked = True
            user.is_active = False
        else:
            user.is_blocked = False
            user.is_active = True
        user.save()
        return redirect('mailing:home')
