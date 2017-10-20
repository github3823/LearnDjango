from django.contrib import admin
from app01 import models
from blog import models as bldb

class bl(admin.ModelAdmin):
    list_display = ('headline','n_comments','n_pingbacks',)
# Register your models here.

class bk(admin.ModelAdmin):
    list_display = ('name','publisher','publish_date',)
    list_editable = ('publish_date',)
admin.site.register(models.Athor)
admin.site.register(models.Publisher)
admin.site.register(models.Book,bk)

admin.site.register(bldb.Author)
admin.site.register(bldb.Blog)
admin.site.register(bldb.Entry,bl)