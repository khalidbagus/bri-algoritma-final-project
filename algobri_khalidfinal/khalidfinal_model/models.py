from django.db import models

# Create your models here.
class BBRIRecord(models.Model):
    datetime = models.DateTimeField(primary_key=True)
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField()
    adj_close_price = models.FloatField()
    volume = models.BigIntegerField()

    def __str__(self):
        return f"{self.datetime} - Close: {self.close_price}"