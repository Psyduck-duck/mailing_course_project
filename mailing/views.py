from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.utils import timezone
from .models import Recipient, Message, Mailing, SendAttempt
from .forms import RecipientForm, MessageForm, MailingForm


# CRUD для получателей (Recipient)

class RecipientListView(LoginRequiredMixin, generic.ListView):
    model = Recipient
    template_name = 'mailing/recipient_list.html'
    context_object_name = 'recipients'
    login_url = reverse_lazy('users:login')


class RecipientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipient_list')
    login_url = reverse_lazy('users:login')


class RecipientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipient_list')
    login_url = reverse_lazy('users:login')


class RecipientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Recipient
    template_name = 'mailing/recipient_confirm_delete.html'
    success_url = reverse_lazy('mailing:recipient_list')
    login_url = reverse_lazy('users:login')


# CRUD для сообщений (Message)

class MessageListView(LoginRequiredMixin, generic.ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'
    login_url = reverse_lazy('users:login')


class MessageCreateView(LoginRequiredMixin, generic.CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')
    login_url = reverse_lazy('users:login')

    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            responce = form.save(commit=False)
            responce.owner = request.user
            responce.save()
            return redirect('mailing:message_list')


class MessageUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')
    login_url = reverse_lazy('users:login')


class MessageDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:message_list')
    login_url = reverse_lazy('users:login')


# CRUD для рассылок (Mailing)

class MailingListView(LoginRequiredMixin, generic.ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'
    login_url = reverse_lazy('users:login')


class MailingCreateView(LoginRequiredMixin, generic.CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')
    login_url = reverse_lazy('users:login')

    def post(self, request):
        form = MailingForm(request.POST)
        if form.is_valid():
            responce = form.save(commit=False)
            responce.owner = request.user
            responce.save()
            return redirect('mailing:mailing_list')


class MailingUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')
    login_url = reverse_lazy('users:login')


class MailingDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')
    login_url = reverse_lazy('users:login')


class MailingStatusView(LoginRequiredMixin, generic.DetailView):
    model = Mailing
    template_name = 'mailing/mailing_status.html'
    login_url = reverse_lazy('users:login')


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
                    'from@example.com',  # email from
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
                server_response=server_response
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
        context['total_mailings'] = Mailing.objects.count()
        context['active_mailings'] = Mailing.objects.filter(status='Запущена').count()
        context['unique_recipients'] = Recipient.objects.count()
        return context