from django.contrib import admin
from .models import Author, Genre, AppealFactor, Work, Item, Series

admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(AppealFactor)
admin.site.register(Series)
admin.site.register(Work)
admin.site.register(Item)
