from django.core.management.base import BaseCommand
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Add test products to the db'

    def handle(self, *args, **options):
        CustomUser.objects.all().delete()
