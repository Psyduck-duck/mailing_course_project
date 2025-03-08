from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Add permissions to the db'

    def handle(self, *args, **options):

        call_command('loaddata', 'perms.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))
