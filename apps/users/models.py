from django.db import models


# Create your models here.
class CustomUser(models.Model):
    first_name = models.CharField(
        max_length=64,
        verbose_name="Imię"
        )
    last_name = models.CharField(
        max_length=100,
        verbose_name="Nazwisko"
    )
    active = models.BooleanField(
        default=True,
        verbose_name="Aktywny"
    )

    def __str__(self):
        return self.first_name + " " + self.last_name
