import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q


class Work(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title_preferred = models.TextField()
    wikidata_id = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "work"
        constraints = [
            models.CheckConstraint(
                condition=~Q(title_preferred=""),
                name="ck_work_title_preferred_not_blank",
            ),
        ]

    def __str__(self):
        return self.title_preferred


class Expression(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    work = models.ForeignKey(
        Work,
        on_delete=models.RESTRICT,
        related_name="expressions",
    )
    language_code = models.CharField(max_length=32)
    expression_type = models.CharField(max_length=64)

    class Meta:
        db_table = "expression"
        constraints = [
            models.CheckConstraint(
                condition=~Q(language_code=""),
                name="ck_expression_language_code_not_blank",
            ),
            models.CheckConstraint(
                condition=~Q(expression_type=""),
                name="ck_expression_type_not_blank",
            ),
        ]

    def __str__(self):
        return f"{self.work.title_preferred} [{self.language_code}, {self.expression_type}]"


class Manifestation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    isbn = models.CharField(max_length=32, null=True, blank=True)
    publication_year = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(3000)],
    )
    edition_statement = models.TextField(null=True, blank=True)
    nb_sesamid = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "manifestation"

    def __str__(self):
        parts = []
        if self.isbn:
            parts.append(self.isbn)
        if self.publication_year is not None:
            parts.append(str(self.publication_year))
        if self.edition_statement:
            parts.append(self.edition_statement)
        return " | ".join(parts) if parts else str(self.id)


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    manifestation = models.ForeignKey(
        Manifestation,
        on_delete=models.RESTRICT,
        related_name="items",
    )
    shelf_location = models.CharField(max_length=255, null=True, blank=True)
    provenance_notes = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "item"

    def __str__(self):
        if self.shelf_location:
            return f"{self.shelf_location} ({self.id})"
        return str(self.id)


class ExpressionManifestation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expression = models.ForeignKey(
        Expression,
        on_delete=models.RESTRICT,
        related_name="expression_manifestations",
    )
    manifestation = models.ForeignKey(
        Manifestation,
        on_delete=models.RESTRICT,
        related_name="expression_manifestations",
    )
    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = "expression_manifestation"
        constraints = [
            models.UniqueConstraint(
                fields=["expression", "manifestation"],
                name="uq_expression_manifestation",
            ),
            models.UniqueConstraint(
                fields=["manifestation"],
                condition=Q(is_primary=True),
                name="uq_expression_manifestation_one_primary",
            ),
        ]

    def __str__(self):
        return f"{self.expression_id} -> {self.manifestation_id}"