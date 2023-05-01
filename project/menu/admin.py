from django.contrib import admin
from .models import *


@admin.register(Submenu)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_submenu')
    list_filter = ('menu',)
    fieldsets = (
        ('Add new item', {
            'description': "Parent should be a menu or item",
            'fields': (('menu', 'parent_submenu'), 'name', 'slug')
        }),
    )
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}
