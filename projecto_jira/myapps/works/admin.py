""" Configuraciones del admin de django """

# Django
from django.contrib import admin

# Modelos
from myapps.works.models import Work

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('name','description','state','admin','responsible','created')
    list_filter = ('state','created','modified')
