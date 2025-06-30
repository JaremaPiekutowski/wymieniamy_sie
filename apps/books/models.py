from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(
        max_length=500,
        verbose_name="Tytuł",
        db_index=True  # Add index for title searches
        )
    author = models.CharField(
        null=True,
        blank=True,
        max_length=500,
        verbose_name="Nazwisko i imię autora/ki",
        db_index=True  # Add index for author searches
    )
    # Genre - foreign key to BookGenre
    genre = models.ForeignKey(
        'BookGenre',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Gatunek",
    )
    user = models.ForeignKey(
        "users.CustomUser",
        null=True,
        blank=True,
        related_name="books",
        on_delete=models.SET_NULL,
        verbose_name="Wrzucający",
    )
    date_added = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data dodania",
        db_index=True  # Add index for date sorting and filtering
    )
    review = models.URLField(
        max_length=1000,
        null=True,
        blank=True,
        verbose_name="Recenzja",
    )

    class Meta:
        indexes = [
            models.Index(fields=['title', 'author']),  # Composite index for title+author lookups
            models.Index(fields=['-date_added']),  # Index for reverse date ordering
        ]

    def __str__(self):
        return self.title


class BookGenre(models.Model):
    name = models.CharField(
        max_length=500,
        verbose_name="Gatunek",
        db_index=True  # Add index for genre name lookups
    )

    def __str__(self):
        return self.name
