from django.db import models

class Agent(models.Model):
    name = models.CharField(max_length=255)
    uri = models.URLField(max_length=500, null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Role(models.Model):
    # Selve koden (f.eks. 'aut')
    code = models.CharField(max_length=20) 
    
    # Menneskelig lesbar etikett (f.eks. 'Forfatter')
    label = models.CharField(max_length=100)
    
    # Angir kilden (f.eks. 'LOC', 'RDA', 'Local')
    vocabulary = models.CharField(max_length=50, default='LOC')
    
    # URI for Linked Data-kompatibilitet (f.eks. http://id.loc.gov/vocabulary/relators/aut)
    uri = models.URLField(blank=True, null=True, unique=True)

    class Meta:
        # Sikrer at kombinasjonen av kode og vokabular er unik
        unique_together = ('code', 'vocabulary')

    def __str__(self):
        return f"{self.label} [{self.vocabulary}]"

class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='subgenres'
    )

    def __str__(self):
        return f"{self.parent.name} > {self.name}" if self.parent else self.name

class AppealFactor(models.Model):
    CATEGORY_CHOICES = [
        ('Pace', 'Pace'),
        ('Tone', 'Tone'),
        ('Writing Style', 'Writing Style'),
        ('Characterization', 'Characterization'),
        ('Storyline', 'Storyline'),
        ('Frame', 'Frame'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='subfactors'
    )

    def __str__(self):
        hierarchy = f"{self.parent.name} > " if self.parent else ""
        return f"{self.category}: {hierarchy}{self.name}"

class Work(models.Model):
    preferred_title = models.CharField(max_length=255)
    original_language = models.CharField(max_length=100, null=True, blank=True)
    uri = models.URLField(max_length=500, null=True, blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    appeal_factors = models.ManyToManyField(AppealFactor, blank=True)

    def __str__(self):
        return self.preferred_title

class Expression(models.Model):
    work = models.ForeignKey(Work, on_delete=models.SET_NULL, null=True, related_name='expressions')
    title_on_expression = models.CharField(max_length=255)
    language = models.CharField(max_length=100)
    content_type = models.CharField(max_length=100, default="text")
    
    def __str__(self):
        return f"{self.title_on_expression} ({self.language})"

class Contribution(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True)
    work = models.ForeignKey(Work, on_delete=models.SET_NULL, null=True, blank=True)
    expression = models.ForeignKey(Expression, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

class Manifestation(models.Model):
    expression = models.ForeignKey(Expression, on_delete=models.SET_NULL, null=True, related_name='manifestations')
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)
    publisher = models.CharField(max_length=255, null=True, blank=True)
    publication_year = models.IntegerField(null=True, blank=True)
    format = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.isbn or 'No ISBN'} - {self.publisher}"

class Item(models.Model):
    manifestation = models.ForeignKey(Manifestation, on_delete=models.SET_NULL, null=True, related_name='items')
    is_loaned = models.BooleanField(default=False)
    condition = models.TextField(null=True, blank=True)
    accession_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Item of {self.manifestation}"