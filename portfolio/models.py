from django.db import models
from django.conf import settings

# Create your models here.
class Company(models.Model):
	ticker = models.CharField(max_length=10, null=True)
	avg_price  = models.FloatField(null=True)
	nbr_shares = models.IntegerField(null = True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)

	def __str__(self):
		return self.ticker.upper()