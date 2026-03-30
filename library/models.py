import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q, F
from django.core.validators import RegexValidator


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
        return f"{self.title_preferred} [{str(self.id)[:8]}]"


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
    title = models.CharField(max_length=255, blank=True, null=True)
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
        ordering = ["title", "publication_year", "isbn"]

    def __str__(self):
        parts = []
        if self.title:
            parts.append(self.title)
        if self.publication_year is not None:
            parts.append(str(self.publication_year))
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

class Agent(models.Model):
    PERSON = "person"
    COLLECTIVE_AGENT = "collective_agent"

    AGENT_TYPE_CHOICES = [
        (PERSON, "Person"),
        (COLLECTIVE_AGENT, "Collective agent"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    agent_type = models.CharField(max_length=32, choices=AGENT_TYPE_CHOICES)
    wikidata_id = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r"^Q\d+$",
                message="wikidata_id må være på formen Q12345.",
            )
        ],
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Role(models.Model):
    code = models.CharField(primary_key=True, max_length=100)
    label = models.CharField(max_length=255)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.label}"


class Contribution(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    agent = models.ForeignKey(
        Agent,
        on_delete=models.RESTRICT,
        related_name="contributions",
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.RESTRICT,
        related_name="contributions",
    )

    work = models.ForeignKey(
        "Work",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contributions",
    )
    expression = models.ForeignKey(
        "Expression",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contributions",
    )
    manifestation = models.ForeignKey(
        "Manifestation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contributions",
    )
    item = models.ForeignKey(
        "Item",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contributions",
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="contribution_exactly_one_target",
                condition=(
                    (
                        Q(work__isnull=False)
                        & Q(expression__isnull=True)
                        & Q(manifestation__isnull=True)
                        & Q(item__isnull=True)
                    )
                    | (
                        Q(work__isnull=True)
                        & Q(expression__isnull=False)
                        & Q(manifestation__isnull=True)
                        & Q(item__isnull=True)
                    )
                    | (
                        Q(work__isnull=True)
                        & Q(expression__isnull=True)
                        & Q(manifestation__isnull=False)
                        & Q(item__isnull=True)
                    )
                    | (
                        Q(work__isnull=True)
                        & Q(expression__isnull=True)
                        & Q(manifestation__isnull=True)
                        & Q(item__isnull=False)
                    )
                ),
            ),
            models.UniqueConstraint(
                fields=["agent", "role", "work"],
                condition=Q(work__isnull=False),
                name="unique_contribution_agent_role_work",
            ),
            models.UniqueConstraint(
                fields=["agent", "role", "expression"],
                condition=Q(expression__isnull=False),
                name="unique_contribution_agent_role_expression",
            ),
            models.UniqueConstraint(
                fields=["agent", "role", "manifestation"],
                condition=Q(manifestation__isnull=False),
                name="unique_contribution_agent_role_manifestation",
            ),
            models.UniqueConstraint(
                fields=["agent", "role", "item"],
                condition=Q(item__isnull=False),
                name="unique_contribution_agent_role_item",
            ),
        ]
        ordering = ["role__code", "agent__name"]

    def __str__(self):
        target = self.work or self.expression or self.manifestation or self.item
        return f"{self.agent} - {self.role} - {target}"

class WorkRelationship(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    source_work = models.ForeignKey(
        "Work",
        on_delete=models.RESTRICT,
        related_name="outgoing_work_relationships",
    )
    target_work = models.ForeignKey(
        "Work",
        on_delete=models.RESTRICT,
        related_name="incoming_work_relationships",
    )
    relation_type = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="workrelationship_no_self_relation",
                condition=~Q(source_work=F("target_work")),
            ),
            models.UniqueConstraint(
                fields=["source_work", "target_work", "relation_type"],
                name="unique_workrelationship_source_target_type",
            ),
        ]
        ordering = ["relation_type", "source_work", "target_work"]

    def __str__(self):
        return f"{self.source_work} - {self.relation_type} -> {self.target_work}"

class Series(models.Model):
    NARRATIVE = "narrative"
    PUBLISHER_SERIES = "publisher_series"

    SERIES_TYPE_CHOICES = [
        (NARRATIVE, "Narrative"),
        (PUBLISHER_SERIES, "Publisher series"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    series_type = models.CharField(max_length=32, choices=SERIES_TYPE_CHOICES)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} [{self.series_type}]"


class SeriesMembership(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    series = models.ForeignKey(
        Series,
        on_delete=models.RESTRICT,
        related_name="memberships",
    )
    work = models.ForeignKey(
        "Work",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="series_memberships",
    )
    manifestation = models.ForeignKey(
        "Manifestation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="series_memberships",
    )
    part_number = models.IntegerField(null=True, blank=True)
    part_display = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="seriesmembership_exactly_one_target",
                condition=(
                    (Q(work__isnull=False) & Q(manifestation__isnull=True))
                    | (Q(work__isnull=True) & Q(manifestation__isnull=False))
                ),
            ),
            models.UniqueConstraint(
                fields=["series", "work"],
                condition=Q(work__isnull=False),
                name="unique_seriesmembership_series_work",
            ),
            models.UniqueConstraint(
                fields=["series", "manifestation"],
                condition=Q(manifestation__isnull=False),
                name="unique_seriesmembership_series_manifestation",
            ),
        ]
        ordering = ["series__title", "part_number", "part_display"]

    def __str__(self):
        target = self.work or self.manifestation
        if self.part_display:
            return f"{self.series} - {target} ({self.part_display})"
        if self.part_number is not None:
            return f"{self.series} - {target} ({self.part_number})"
        return f"{self.series} - {target}"

class Character(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class WorkCharacter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    work = models.ForeignKey(
        "Work",
        on_delete=models.RESTRICT,
        related_name="work_characters",
    )
    character = models.ForeignKey(
        Character,
        on_delete=models.RESTRICT,
        related_name="work_characters",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["work", "character"],
                name="unique_workcharacter_work_character",
            ),
        ]
        ordering = ["work", "character"]

    def __str__(self):
        return f"{self.work} - {self.character}"

class Genre(models.Model):
    code = models.CharField(primary_key=True, max_length=100)
    label = models.CharField(max_length=255)
    parent_genre = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="child_genres",
    )

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.label}"


class WorkGenre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    work = models.ForeignKey(
        "Work",
        on_delete=models.RESTRICT,
        related_name="work_genres",
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.RESTRICT,
        related_name="work_genres",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["work", "genre"],
                name="unique_workgenre_work_genre",
            ),
        ]
        ordering = ["work", "genre"]

    def __str__(self):
        return f"{self.work} - {self.genre}"

class AppealFactor(models.Model):
    code = models.CharField(primary_key=True, max_length=100)
    label = models.CharField(max_length=255)
    parent_appeal_factor = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="child_appeal_factors",
    )
    definition = models.TextField(blank=True, null=True)
    scope_note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.label}"


class WorkAppealFactor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    work = models.ForeignKey(
        "Work",
        on_delete=models.RESTRICT,
        related_name="work_appeal_factors",
    )
    appeal_factor = models.ForeignKey(
        AppealFactor,
        on_delete=models.RESTRICT,
        related_name="work_appeal_factors",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["work", "appeal_factor"],
                name="unique_workappealfactor_work_appealfactor",
            ),
        ]
        ordering = ["work", "appeal_factor"]

    def __str__(self):
        return f"{self.work} - {self.appeal_factor}"