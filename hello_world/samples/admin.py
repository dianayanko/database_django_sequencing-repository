"""
Django admin configuration for samples app.
Core biological entity management: Organism, Donor, Sample, TissueType.
"""
from django.contrib import admin
from hello_world.admin_site import admin_site
from .models import Organism, TissueType, Donor, Sample


# ============================================================================
# CORE BIOLOGICAL ENTITIES
# ============================================================================

class OrganismAdmin(admin.ModelAdmin):
    """Manage biological organisms (species)."""
    list_display = ('common_name', 'scientific_name', 'taxonomy_id')
    list_filter = ('taxonomy_id', 'created_at')
    search_fields = ('common_name', 'scientific_name', 'taxonomy_id')
    ordering = ('scientific_name',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('scientific_name', 'common_name', 'taxonomy_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


class TissueTypeAdmin(admin.ModelAdmin):
    """Manage tissue type classifications."""
    list_display = ('name', 'ontology_id', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'ontology_id')
    ordering = ('name',)

    fieldsets = (
        ('Tissue Information', {
            'fields': ('name', 'description', 'ontology_id')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at',)


class SampleInline(admin.TabularInline):
    """Inline display of samples for a donor."""
    model = Sample
    extra = 0
    fields = ('sample_id', 'tissue_type', 'sample_type', 'collection_date', 'storage_conditions')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ['-created_at']


class DonorAdmin(admin.ModelAdmin):
    """Manage biological donors/individuals."""
    list_display = ('donor_id', 'organism', 'age', 'sex', 'disease_state', 'sample_count')
    list_filter = ('organism', 'sex', 'disease_state', 'created_at')
    search_fields = ('donor_id', 'organism__scientific_name')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [SampleInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('donor_id', 'organism', 'age', 'sex')
        }),
        ('Health & Biology', {
            'fields': ('disease_state', 'genotype', 'phenotype')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def sample_count(self, obj):
        """Display count of samples for this donor."""
        return obj.sample_set.count()
    sample_count.short_description = 'Sample Count'


class SampleAdmin(admin.ModelAdmin):
    """Manage biological samples."""
    list_display = ('sample_id', 'donor', 'tissue_type', 'sample_type', 'storage_conditions', 'created_at')
    list_filter = ('sample_type', 'tissue_type', 'created_at')
    search_fields = ('sample_id', 'donor__donor_id', 'donor__organism__common_name')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Sample Information', {
            'fields': ('sample_id', 'donor', 'tissue_type', 'sample_type')
        }),
        ('Collection Details', {
            'fields': ('collection_date', 'passage_number', 'storage_conditions')
        }),
        ('Characteristics', {
            'fields': ('cell_count', 'viability')
        }),
        ('Documentation', {
            'fields': ('description', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# Register with custom admin site
admin_site.register(Organism, OrganismAdmin)
admin_site.register(TissueType, TissueTypeAdmin)
admin_site.register(Donor, DonorAdmin)
admin_site.register(Sample, SampleAdmin)
