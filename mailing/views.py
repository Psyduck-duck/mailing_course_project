from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from .models import Recipient, Message, Mailing, SendAttempt
from .forms import RecipientForm, MessageForm, MailingForm
from .services import CustomUserService

# CRUD для получателей (Recipient)


class RecipientListView(LoginRequiredMixin, generic.ListView):
    model = Recipient
    template_name = 'mailing/recipient_list.html'
    context_object_name = 'recipients'
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.has_perm('mailing.can_see_all_recipients'):
            queryset = Recipient.objects.all()
        else:
            queryset = Recipient.objects.filter(owner_id=user_id)
        return queryset


class RecipientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipient_list')
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        recipient = form.save(commit=False)
        user = self.request.user
        recipient.owner = user
        recipient.save()
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipient_list')
    login_url = reverse_lazy('users:login')

    def get_form_class(self):
        user = self.request.user
        if user.has_perm('mailing.update_recipient') or self.object.owner == user:
            return RecipientForm

        raise PermissionDenied('У вас нет прав для изменения получателя')


class RecipientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Recipient
    template_name = 'mailing/recipient_confirm_delete.html'
    success_url = reverse_lazy('mailing:recipient_list')
    login_url = reverse_lazy('users:login')

    def get(self, request, pk):
        recipient = get_object_or_404(Recipient, id=pk)
        if request.user.has_perm('mailing.delete_message') or recipient.owner == request.user:
            return super().get(request, pk)
        return HttpResponseForbidden('У вас нет прав для удаления получателя')

    def post(self, request, pk):

        recipient = get_object_or_404(Recipient, id=pk)
        if request.user.has_perm('mailing.delete_recipient') or recipient.owner == request.user:
            recipient.delete()
            return redirect('mailing:recipient_list')
        return HttpResponseForbidden('У вас нет прав для удаления получателя')

# CRUD для сообщений (Message)


class MessageListView(LoginRequiredMixin, generic.ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.has_perm('mailing.can_see_all_messages'):
            queryset = Message.objects.all()
        else:
            queryset = Message.objects.filter(owner_id=user_id)
        return queryset


class MessageCreateView(LoginRequiredMixin, generic.CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        message = form.save(commit=False)
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')
    login_url = reverse_lazy('users:login')

    def get_form_class(self):
        user = self.request.user
        if user.has_perm('mailing.update_message') or self.object.owner == user:
            return MessageForm

        raise PermissionDenied('У вас нет прав для изменения сообщения')


class MessageDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:message_list')
    login_url = reverse_lazy('users:login')

    def get(self, request, pk):
        message = get_object_or_404(Message, id=pk)
        if request.user.has_perm('mailing.delete_message') or message.owner == request.user:
            return super().get(request, pk)
        return HttpResponseForbidden('У вас нет прав для удаления сообщения')

    def post(self, request, pk):

        message = get_object_or_404(Message, id=pk)
        if request.user.has_perm('mailing.delete_message') or message.owner == request.user:
            message.delete()
            return redirect('mailing:message_list')
        return HttpResponseForbidden('У вас нет прав для удаления сообщения')


# CRUD для рассылок (Mailing)

class MailingListView(LoginRequiredMixin, generic.ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.has_perm('mailing.can_see_all_mailing'):
            queryset = Mailing.objects.all()
        else:
            queryset = Mailing.objects.filter(owner_id=user_id)
        return queryset


class MailingCreateView(LoginRequiredMixin, generic.CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        mailing = form.save(commit=False)
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')
    login_url = reverse_lazy('users:login')

    def get_form_class(self):
        user = self.request.user
        if user.has_perm('mailing.update_mailing') or self.object.owner == user:
            return MailingForm

        raise PermissionDenied('У вас нет прав для изменения рассылки')


class MailingDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')
    login_url = reverse_lazy('users:login')

    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, id=pk)
        if request.user.has_perm('mailing.delete_mailing') or mailing.owner == request.user:
            return super().get(request, pk)
        return HttpResponseForbidden('У вас нет прав для удаления рассылки')

    def post(self, request, pk):

        mailing = get_object_or_404(Mailing, id=pk)
        if request.user.has_perm('mailing.delete_mailing') or mailing.owner == request.user:
            mailing.delete()
            return redirect('mailing:mailing_list')
        return HttpResponseForbidden('У вас нет прав для удаления рассылки')


class MailingStatusView(LoginRequiredMixin, generic.DetailView):
    model = Mailing
    template_name = 'mailing/mailing_status.html'
    login_url = reverse_lazy('users:login')

    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, id=pk)
        if request.user.has_perm('mailing.view_mailing') or mailing.owner == request.user:
            return super().get(request, pk)
        return HttpResponseForbidden('У вас нет прав для просмотра деталей рассылки')


# Генерация отчета и отправка рассылки

class SendMailingView(generic.View):
    def get(self, request, mailing_id):
        mailing = self.get_object(mailing_id)
        recipients = mailing.recipients.all()

        # Инициация отправки
        for recipient in recipients:
            try:
                send_mail(
                    mailing.message.subject,
                    mailing.message.body,
                    EMAIL_HOST_USER,
                    [recipient.email],
                    fail_silently=False,
                )
                status = 'Успешно'
                server_response = 'Письмо отправлено успешно.'
            except Exception as e:
                status = 'Не успешно'
                server_response = str(e)

            # Сохранение попытки рассылки
            SendAttempt.objects.create(
                mailing=mailing,
                status=status,
                recipient=recipient,
                server_response=server_response,
                owner=request.user
            )

        # Обновление статуса рассылки
        if mailing.status == 'Создана':
            mailing.status = 'Запущена'
            mailing.first_sent_at = timezone.now()
            mailing.save()

        return render(request, 'mailing/mailing_status.html', {'mailing': mailing})

    @staticmethod
    def get_object(mailing_id):
        return Mailing.objects.get(id=mailing_id)


# Главная страница

class HomeView(generic.TemplateView):
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_send_message'] = SendAttempt.objects.filter(status='Успешно').count()
        if self.request.user.is_authenticated:
            user_id = self.request.user.id

            if self.request.user.has_perm('users.can_see_all_users'):
                context['users_statistic_list'] = CustomUserService.users_statistic_list()
            else:
                context['users_statistic_list'] = CustomUserService.users_statistic_list(user_id)
        return context


class OffMailingView(LoginRequiredMixin, generic.View):
    model = Mailing
    template_name = 'mailing/mailing_off_confirm.html'
    success_url = reverse_lazy('mailing:mailing_list')
    login_url = reverse_lazy('users:login')
    context_object_name = 'mailing'

    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, id=pk)
        if not request.user.has_perm('mailing.can_turn_off_mailing'):
            return HttpResponseForbidden('У вас нет прав для выключения рассылки')
        return render(request, 'mailing/mailing_off_confirm.html', {'mailing': mailing})

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, id=pk)
        if not request.user.has_perm('mailing.can_turn_off_mailing'):
            return HttpResponseForbidden('У вас нет прав для выключения рассылки')
        mailing.status = 'Отключена'
        mailing.save()
        return redirect('mailing:mailing_list')
