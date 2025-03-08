from django.urls import path
from .views import (
    HomeView, SendMailingView,
    RecipientListView, RecipientCreateView, RecipientUpdateView, RecipientDeleteView,
    MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView,
    MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView, MailingStatusView, OffMailingView
)

app_name = 'mailing'

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),

    # Recipient URLs
    path('recipients/', RecipientListView.as_view(), name='recipient_list'),
    path('recipients/create/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipients/update/<int:pk>/', RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipients/delete/<int:pk>/', RecipientDeleteView.as_view(), name='recipient_delete'),

    # Message URLs
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),

    # Mailing URLs
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailings/status/<int:pk>/', MailingStatusView.as_view(), name='mailing_status'),
    path('mailings/off/<int:pk>/', OffMailingView.as_view(), name='mailing_off'),

    # Send Mailing
    path('send-mailing/<int:mailing_id>/', SendMailingView.as_view(), name='send_mailing'),
]
