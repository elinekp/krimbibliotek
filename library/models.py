from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)
    biography = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Work(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='works')
    summary = models.TextField(blank=True)
    original_publication_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title