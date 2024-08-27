import csv
from django.core.management.base import BaseCommand
from ...models import BBRIRecord
from datetime import datetime

class Command(BaseCommand):
    help = 'Load BBRI data from CSV file'

    def handle(self, *args, **kwargs):
        with open('khalidfinal_model/management/commands/bbri.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                BBRIRecord.objects.create(
                    datetime=datetime.fromisoformat(row['Datetime']),
                    open_price=float(row['Open']),
                    high_price=float(row['High']),
                    low_price=float(row['Low']),
                    close_price=float(row['Close']),
                    adj_close_price=float(row['Adj Close']),
                    volume=int(row['Volume'])
                )
        self.stdout.write(self.style.SUCCESS('Data loaded successfully!'))
