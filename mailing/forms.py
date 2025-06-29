from django import forms
from .models import Recipient, Message, Mailing


class RecipientForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Почта получателя'})
        self.fields['full_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Полное имя получателя'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Комментарий'})

    class Meta:
        model = Recipient
        fields = ['email', 'full_name', 'comment']


class MessageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Тема письма'})
        self.fields['body'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Сообщение'})

    class Meta:
        model = Message
        fields = ['subject', 'body']


class MailingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_sent_at'].widget.attrs.update({'class': 'form-control', 'placeholder': 'YYYY-MM-DD hh:mm:ss'})
        self.fields['end_at'].widget.attrs.update({'class': 'form-control', 'placeholder': 'YYYY-MM-DD hh:mm:ss'})
        self.fields['message'].widget.attrs.update({'class': 'form-control'})
        self.fields['recipients'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Mailing
        fields = ['first_sent_at', 'end_at', 'message', 'recipients']
