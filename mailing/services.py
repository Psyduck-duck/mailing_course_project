from .models import Message, Mailing, Recipient, SendAttempt


class SendAttemptService:

    @staticmethod
    def get_success_attempts_count(user_id):
        """ метод для получения счетчика успешных попыток отправок пользоватяля """

        success_attempts_count = SendAttempt.objects.filter(status='Успешно', owner_id=user_id).count()
        return success_attempts_count

    @staticmethod
    def get_unsuccess_attempts_count(user_id):
        """ метод для получения счетчика неуспешных попыток отправок пользоватяля """

        unsuccess_attempts_count = SendAttempt.objects.filter(status='Не успешно', owner=user_id).count()
        return unsuccess_attempts_count
