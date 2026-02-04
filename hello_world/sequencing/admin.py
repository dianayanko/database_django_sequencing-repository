"""
Django admin configuration for sequencing app.
Core sequencing entities: SequencingPlatform, SequencingProject, LibraryPreparation, SequencingRun.
"""
from django.contrib import admin
from hello_world.admin_site import admin_site
from .models import SequencingPlatform, SequencingProject, LibraryPreparation, SequencingRun


# ============================================================================
# TECHNICAL ENTITIES - Supporting Infrastructure
# ============================================================================

class SequencingPlatformAdmin(admin.ModelAdmin):
    """Manage sequencing platforms/instruments available in the facility."""
    list_display = ('name', 'platform_type', 'manufacturer', 'read_type', 'instrument_model')
    list_filter = ('platform_type', 'read_type', 'manufacturer')
    search_fields = ('name', 'manufacturer', 'instrument_model')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Platform Information', {
            'fields': ('name', 'platform_type', 'manufacturer', 'instrument_model')
        }),
        ('Capabilities', {
            'fields': ('read_type', 'read_length_min', 'read_length_max')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ============================================================================
# CORE SEQUENCING ENTITIES
# ============================================================================

class SequencingProjectAdmin(admin.ModelAdmin):
    """Manage sequencing projects that contain samples and runs."""
    list_display = ('project_id', 'title', 'project_type', 'status', 'pi_name', 'sample_count')
    list_filter = ('project_type', 'status', 'created_at')
    search_fields = ('project_id', 'title', 'pi_name', 'institution')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('samples',)

    fieldsets = (
        ('Project Information', {
            'fields': ('project_id', 'title', 'description')
        }),
        ('Project Details', {
            'fields': ('project_type', 'pi_name', 'institution')
        }),
        ('Status & Timeline', {
            'fields': ('status', 'start_date', 'completion_date')
        }),
        ('Samples', {
            'fields': ('samples',)
        }),
        ('Documentation', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def sample_count(self, obj):
        """Display count of samples in this project."""
        return obj.samples.count()
    sample_count.short_description = 'Samples'


class LibraryPreparationInline(admin.StackedInline):
    """Inline display of library preparation for a sequencing run."""
    model = LibraryPreparation
    extra = 0
    fields = ('library_id', 'library_kit', 'qc_status', 'insert_size_bp', 'prep_date')
    readonly_fields = ('created_at', 'updated_at')


class LibraryPreparationAdmin(admin.ModelAdmin):
    """Manage library preparation details (before sequencing)."""
    list_display = ('library_id', 'library_kit', 'qc_status', 'prep_date', 'insert_size_bp')
    list_filter = ('library_kit', 'qc_status', 'prep_date', 'created_at')
    search_fields = ('library_id', 'index_name', 'index_sequence')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Library Information', {
            'fields': ('library_id', 'library_kit')
        }),
        ('Library Characteristics', {
            'fields': ('insert_size_bp', 'fragment_size_bp', 'library_concentration', 'library_volume_ul')
        }),
        ('QC Metrics', {
            'fields': ('qc_status', 'rna_integrity_number', 'dna_integrity')
        }),
        ('Indexing', {
            'fields': ('index_name', 'index_sequence')
        }),
        ('Preparation Details', {
            'fields': ('prep_date', 'technician')
        }),
        ('Documentation', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class SequencingRunAdmin(admin.ModelAdmin):
    """Manage sequencing runs - the actual execution of sequencing."""
    list_display = ('run_id', 'project', 'sample', 'platform', 'status', 'run_date', 'total_reads')
    list_filter = ('status', 'platform', 'run_date', 'created_at')
    search_fields = ('run_id', 'sample__sample_id', 'flowcell_id', 'project__project_id')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Run Information', {
            'fields': ('run_id', 'project', 'sample', 'platform', 'library_preparation')
        }),
        ('Run Details', {
            'fields': ('run_date', 'status', 'flowcell_id')
        }),
        ('Sequencing Results', {
            'fields': ('total_reads', 'total_bases', 'q30_percentage', 'mean_read_length')
        }),
        ('Completion', {
            'fields': ('completion_date', 'technician')
        }),
        ('Documentation', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# Register with custom admin site
admin_site.register(SequencingPlatform, SequencingPlatformAdmin)
admin_site.register(SequencingProject, SequencingProjectAdmin)
admin_site.register(LibraryPreparation, LibraryPreparationAdmin)
admin_site.register(SequencingRun, SequencingRunAdmin)
