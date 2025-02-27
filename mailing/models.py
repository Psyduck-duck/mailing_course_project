from django.db import models
from users.models import CustomUser


class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name='Адрес электронной почты')
    full_name = models.CharField(max_length=255, verbose_name='Полное имя')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recipients', verbose_name='получатель')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Тема')
    body = models.TextField(verbose_name='Тело сообщения')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='messages', verbose_name='владелец')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('Создана', 'Создана'),
        ('Запущена', 'Запущена'),
        ('Завершена', 'Завершена')
    ]

    first_sent_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата начала отправки')
    end_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата завершения')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Создана', verbose_name='Статус')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    recipients = models.ManyToManyField(Recipient, verbose_name='Получатели')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='mailings', verbose_name='владелец')

    def __str__(self):
        return f"{self.message.subject} - {self.status}"

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class SendAttempt(models.Model):
    STATUS_CHOICES = [
        ('Успешно', 'Успешно'),
        ('Не успешно', 'Не успешно')
    ]

    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name='Время попытки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Статус попытки')
    server_response = models.TextField(blank=True, verbose_name='Ответ сервера')
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, related_name='send_attempts', verbose_name='Получатель')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='send_attempts', verbose_name='Рассылка')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='attempts', verbose_name='владелец')

    def __str__(self):
        return f"Attempt: {self.attempt_time} - {self.status}"

    class Meta:
        verbose_name = 'Попытка отправки'
        verbose_name_plural = 'Попытки отправки'
