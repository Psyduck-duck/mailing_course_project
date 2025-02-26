from django.contrib import admin
from .models import Message, Recipient, Mailing, SendAttempt


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body', 'owner')
    search_fields = ('subject', 'owner')


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('end_at', 'first_sent_at', 'status', 'message', 'owner')
    search_fields = ('status', 'owner')


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'comment')
    search_fields = ('email', 'full_name')


@admin.register(SendAttempt)
class SendAttemptAdmin(admin.ModelAdmin):
    list_display = ('attempt_time', 'status', 'server_response', 'recipient', 'mailing', 'owner')
    search_fields = ('status', 'mailing')
