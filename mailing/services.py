from .models import Message, Mailing, Recipient, SendAttempt
from users.models import CustomUser


class CustomUserService:

    @staticmethod
    def users_statistic_list(user_id=None):
        """ Метод для получения списка статистик пользователей """

        users_statistic_list = []
        if not user_id:
            users_list = CustomUser.objects.all()
        else:
            users_list = CustomUser.objects.filter(id=user_id)
        for user in users_list:
            user_id = user.id
            username = user.username
            user_statistic_dict = {}
            user_statistic_dict['user_id'] = user_id
            user_statistic_dict['username'] = username
            user_statistic_dict['total_mailings'] = Mailing.objects.filter(owner=user_id).count()
            user_statistic_dict['active_mailings'] = Mailing.objects.filter(status='Запущена', owner=user_id).count()
            user_statistic_dict['unique_recipients'] = Recipient.objects.filter(owner=user_id).count()
            user_statistic_dict['total_send_message'] = SendAttempt.objects.filter(status='Успешно', owner=user_id).count()

            users_statistic_list.append(user_statistic_dict)

        return users_statistic_list
