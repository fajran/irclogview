from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Update logs'

    def handle(self, *args, **options):
        from ...utils import update_logs
        update_logs()

