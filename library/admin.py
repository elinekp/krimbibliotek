from django import forms
from django.contrib import admin

from .models import (
    Work,
    Expression,
    Manifestation,
    Item,
    ExpressionManifestation,
    Agent,
    Role,
    Contribution,
    WorkRelationship,
    Series,
    SeriesMembership,
)


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ("title_preferred", "short_id", "wikidata_id")
    search_fields = ("title_preferred", "wikidata_id")

    @admin.display(description="Kort ID")
    def short_id(self, obj):
        return str(obj.id)[:8]


@admin.register(Expression)
class ExpressionAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
    search_fields = ("work__title_preferred",)


@admin.register(Manifestation)
class ManifestationAdmin(admin.ModelAdmin):
    list_display = ("title", "isbn", "publication_year", "nb_sesamid")
    search_fields = ("title", "isbn", "nb_sesamid", "edition_statement")

class ExpressionManifestationAdminForm(forms.ModelForm):
    class Meta:
        model = ExpressionManifestation
        fields = "__all__"
        labels = {
            "expression": "Uttrykk",
            "manifestation": "Manifestasjon",
            "is_primary": "Primær kobling",
        }
        help_texts = {
            "is_primary": (
                "Kryss av når dette er hoveduttrykket for manifestasjonen. "
                "Vanlige utgaver skal normalt ha én primærkobling. "
                "Antologier og samleutgaver kan ha ingen."
            ),
        }


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("__str__", "shelf_location")
    search_fields = ("shelf_location", "provenance_notes")


@admin.register(ExpressionManifestation)
class ExpressionManifestationAdmin(admin.ModelAdmin):
    form = ExpressionManifestationAdminForm
    list_display = ("expression", "manifestation", "is_primary")
    list_filter = ("is_primary",)
    autocomplete_fields = ("expression", "manifestation")


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ("name", "agent_type", "wikidata_id")
    list_filter = ("agent_type",)
    search_fields = ("name", "wikidata_id")


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("code", "label")
    search_fields = ("code", "label")


@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = (
        "agent",
        "role",
        "work",
        "expression",
        "manifestation",
        "item",
    )
    list_filter = ("role",)
    autocomplete_fields = ("agent", "role", "work", "expression", "manifestation", "item")


class WorkRelationshipAdminForm(forms.ModelForm):
    class Meta:
        model = WorkRelationship
        fields = "__all__"
        labels = {
            "source_work": "Opphavsverk (source_work)",
            "target_work": "Avledet verk (target_work)",
            "relation_type": "Relasjonstype",
        }
        help_texts = {
            "source_work": "Det primære verket som det andre verket bygger på.",
            "target_work": "Det sekundære eller avledede verket.",
            "relation_type": (
                "Les alltid relasjonen slik: "
                "target_work (relation_type) source_work. "
                "Eksempel: tegneserieversjonen adaptation_of romanverket."
            ),
        }


@admin.register(WorkRelationship)
class WorkRelationshipAdmin(admin.ModelAdmin):
    form = WorkRelationshipAdminForm
    list_display = (
        "target_work",
        "relation_type",
        "source_work",
        "relationship_reading",
    )
    search_fields = (
        "source_work__title_preferred",
        "target_work__title_preferred",
        "relation_type",
    )
    autocomplete_fields = ("source_work", "target_work")
    list_select_related = ("source_work", "target_work")
    fieldsets = (
        (
            "Relasjon mellom verk",
            {
                "fields": ("source_work", "target_work", "relation_type"),
                "description": (
                    "Registreringsregel: Les alltid relasjonen slik "
                    "<strong>target_work (relation_type) source_work</strong>."
                    "<br><br>"
                    "Eksempel: tegneserieversjonen <code>adaptation_of</code> romanverket."
                ),
            },
        ),
    )

    @admin.display(description="Les som")
    def relationship_reading(self, obj):
        return f"{obj.target_work} {obj.relation_type} {obj.source_work}"


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ("title", "series_type")
    list_filter = ("series_type",)
    search_fields = ("title",)


class SeriesMembershipAdminForm(forms.ModelForm):
    class Meta:
        model = SeriesMembership
        fields = "__all__"
        labels = {
            "series": "Serie",
            "work": "Verk",
            "manifestation": "Manifestasjon",
            "part_number": "Delnummer",
            "part_display": "Visning av del",
        }
        help_texts = {
            "work": "Brukes for narrative serier på verksnivå.",
            "manifestation": "Brukes for serier på manifestasjonsnivå, for eksempel forlagsserie.",
            "part_number": "Valgfritt numerisk serienummer.",
            "part_display": "Valgfri visningstekst, for eksempel 'Del 1' eller 'Bind II'.",
        }


@admin.register(SeriesMembership)
class SeriesMembershipAdmin(admin.ModelAdmin):
    form = SeriesMembershipAdminForm
    list_display = ("series", "work", "manifestation", "part_number", "part_display")
    search_fields = (
        "series__title",
        "work__title_preferred",
        "manifestation__isbn",
        "part_display",
    )
    autocomplete_fields = ("series", "work", "manifestation")
    list_select_related = ("series", "work", "manifestation")
    fieldsets = (
        (
            "Serietilknytning",
            {
                "fields": ("series", "work", "manifestation", "part_number", "part_display"),
                "description": (
                    "Fyll ut enten Verk eller Manifestasjon, men ikke begge."
                ),
            },
        ),
    )