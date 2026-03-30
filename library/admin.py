from django.contrib import admin

from .models import Work, Expression, Manifestation, Item, ExpressionManifestation


admin.site.register(Work)
admin.site.register(Expression)
admin.site.register(Manifestation)
admin.site.register(Item)
admin.site.register(ExpressionManifestation)