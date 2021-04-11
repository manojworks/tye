from django.contrib import admin

from .models import Taxonomy


class TaxonomyAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['parent_id']}),
        ('New Product Information', {'fields': ['taxonomy_id', 'product_description']}),
    ]

    list_display = ('taxonomy_id', 'product_description', 'parent_description')
    #list_filter = ['product_description']
    search_fields = ['product_description']
    list_per_page = 50


admin.site.register(Taxonomy, TaxonomyAdmin)
