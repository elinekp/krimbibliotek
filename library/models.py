from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)
    biography = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Work(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Author, 
        on_delete=models.SET_NULL,  # Endret fra CASCADE
        null=True,                  # Påkrevd for SET_NULL
        blank=True,                 # Tillater at feltet er tomt i skjemaer
        related_name='works'
    )
    summary = models.TextField(blank=True)
    original_publication_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title