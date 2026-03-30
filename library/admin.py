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
)


admin.site.register(Work)
admin.site.register(Expression)
admin.site.register(Manifestation)
admin.site.register(Item)
admin.site.register(ExpressionManifestation)
admin.site.register(Agent)
admin.site.register(Role)
admin.site.register(Contribution)
admin.site.register(WorkRelationship)