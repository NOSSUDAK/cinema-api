import time

from django.core.management import BaseCommand
from django.db import connection, OperationalError

RETRY_PERIOD = 1
MAX_ATTEMPTS = 20

class Command(BaseCommand):
    help = "Waits until db is able to process requests"

    def handle(self, *args, **options):
        attempt = 0
        while attempt < MAX_ATTEMPTS:
            try:
                connection.ensure_connection()
            except OperationalError:
                self.stdout.write(self.style.WARNING(f"Attempt {attempt}. DB is still not ready. Wait for 1 sec..."))
                attempt += 1
                time.sleep(RETRY_PERIOD)
            else:
                self.stdout.write(self.style.SUCCESS("DB is ready to operate"))
                break
        else:
            self.stdout.write(self.style.ERROR("Impossible to connect DB"))
