from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)
    biography = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class AppealFactor(models.Model):
    CATEGORY_CHOICES = [
        ('pace', 'Pace'),
        ('tone', 'Tone'),
        ('character', 'Character'),
        ('style', 'Style'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_category_display()}: {self.name}"

class Work(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Author, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='works'
    )
    genres = models.ManyToManyField(Genre, blank=True, related_name='works')
    appeal_factors = models.ManyToManyField(AppealFactor, blank=True, related_name='works')
    summary = models.TextField(blank=True)
    original_publication_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title