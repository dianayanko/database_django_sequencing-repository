"""
Django admin configuration for files app.
File metadata and associations (typically read-only, created by automated processes).
"""
from django.contrib import admin
from hello_world.admin_site import admin_site
from .models import FileMetadata, FileAssociation


# ============================================================================
# FILE METADATA ENTITIES - READ-ONLY
# ============================================================================

class FileMetadataAdmin(admin.ModelAdmin):
    """View file metadata tracking (read-only - created by pipelines)."""
    list_display = ('file_id', 'file_type', 'read_type', 'file_size_bytes', 'storage_location', 'created_at')
    list_filter = ('file_type', 'read_type', 'storage_location', 'is_compressed', 'created_at')
    search_fields = ('file_id', 'file_path', 'checksum_md5', 'checksum_sha256')
    readonly_fields = ('file_id', 'file_path', 'file_type', 'read_type', 'file_size_bytes', 'file_format_version',
                       'total_reads', 'checksum_md5', 'checksum_sha256', 'is_compressed', 'compression_format',
                       'index_file_path', 'storage_location', 'description', 'notes', 'created_at', 'updated_at')

    fieldsets = (
        ('File Information', {
            'fields': ('file_id', 'file_path', 'file_type', 'read_type')
        }),
        ('File Characteristics', {
            'fields': ('file_size_bytes', 'file_format_version', 'total_reads')
        }),
        ('Data Integrity', {
            'fields': ('checksum_md5', 'checksum_sha256')
        }),
        ('Compression & Indexing', {
            'fields': ('is_compressed', 'compression_format', 'index_file_path')
        }),
        ('Storage', {
            'fields': ('storage_location',)
        }),
        ('Documentation', {
            'fields': ('description', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        """Disable add permission - files are created by pipelines."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Disable delete permission - preserve file records."""
        return False


class FileAssociationAdmin(admin.ModelAdmin):
    """View file associations with runs and analyses (read-only - created by pipelines)."""
    list_display = ('file_metadata', 'sequencing_run', 'analysis', 'file_role', 'created_at')
    list_filter = ('file_role', 'created_at')
    search_fields = ('file_metadata__file_id', 'sequencing_run__run_id', 'analysis__analysis_id')
    readonly_fields = ('file_metadata', 'sequencing_run', 'analysis', 'file_role', 'created_at', 'updated_at')

    fieldsets = (
        ('File Association', {
            'fields': ('file_metadata', 'file_role')
        }),
        ('Associated With', {
            'fields': ('sequencing_run', 'analysis')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        """Disable add permission - associations are created by pipelines."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Disable delete permission - preserve associations."""
        return False


# Register with custom admin site
admin_site.register(FileMetadata, FileMetadataAdmin)
admin_site.register(FileAssociation, FileAssociationAdmin)
