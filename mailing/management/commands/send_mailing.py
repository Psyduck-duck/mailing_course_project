from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError

from config.settings import EMAIL_HOST_USER
from mailing.models import Mailing, SendAttempt


class Command(BaseCommand):
    help = "Отправка рассылки по id, 'send_mailing -<ids:list>'"

    def add_arguments(self, parser):
        parser.add_argument("mailing_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        for mailing_id in options["mailing_ids"]:
            try:
                mailing = Mailing.objects.get(pk=mailing_id)
                message = mailing.message
            except Mailing.DoesNotExist:
                raise CommandError('Mailing "%s" does not exist' % mailing_id)

            recipients = mailing.recipients.all()

            for recipient in recipients:
                try:
                    send_mail(
                        subject=message.subject,
                        message=message.body,
                        from_email=EMAIL_HOST_USER,
                        recipient_list=[recipient.email],
                    )
                    status = 'Успешно'
                    server_response = 'Письмо отправлено успешно.'
                except Exception as e:
                    status = 'Не успешно'
                    server_response = str(e)

                SendAttempt.objects.create(
                    mailing=mailing,
                    status=status,
                    recipient=recipient,
                    server_response=server_response,
                    owner=mailing.owner
                )

                mailing.status = 'Запущена'
                mailing.save()

            self.stdout.write(
                self.style.SUCCESS('Successfully send mailing "%s"' % mailing_id)
            )
