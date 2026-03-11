from django.contrib import admin
from .models import Agent, Role, Genre, AppealFactor, Work, Expression, Contribution, Manifestation, Item

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'uri')
    search_fields = ('name',)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'uri')

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(AppealFactor)
class AppealFactorAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('preferred_title', 'original_language')
    search_fields = ('preferred_title',)

@admin.register(Expression)
class ExpressionAdmin(admin.ModelAdmin):
    list_display = ('title_on_expression', 'language', 'work')
    list_filter = ('language',)

@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ('agent', 'role', 'work', 'expression')
    list_filter = ('role',)

@admin.register(Manifestation)
class ManifestationAdmin(admin.ModelAdmin):
    list_display = ('isbn', 'publisher', 'publication_year')
    search_fields = ('isbn', 'publisher')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('manifestation', 'is_loaned', 'accession_date')
    list_filter = ('is_loaned',)