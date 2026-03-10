from django.contrib import admin
from .models import Author, Work, Genre

admin.site.register(Author)
admin.site.register(Work)
admin.site.register(Genre)