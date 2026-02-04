"""
Django admin configuration for analysis app.
Analysis results and metrics (read-only): QCMetrics, AlignmentMetrics, VariantCallingMetrics, ExpressionMetrics.
"""
from django.contrib import admin
from hello_world.admin_site import admin_site
from .models import (
    Analysis,
    Report,
    QCMetrics,
    AlignmentMetrics,
    VariantCallingMetrics,
    ExpressionMetrics,
)


# ============================================================================
# INLINES FOR ANALYSIS RESULTS (READ-ONLY)
# ============================================================================

class QCMetricsInline(admin.StackedInline):
    model = QCMetrics
    extra = 0
    can_delete = False
    fields = ('total_sequences', 'gc_content_percent', 'qc_status')
    readonly_fields = ('total_sequences', 'gc_content_percent', 'qc_status', 'created_at', 'updated_at')


class AlignmentMetricsInline(admin.StackedInline):
    model = AlignmentMetrics
    extra = 0
    can_delete = False
    fields = ('total_reads', 'mapped_reads', 'mapping_rate_percent')
    readonly_fields = ('total_reads', 'mapped_reads', 'mapping_rate_percent', 'created_at', 'updated_at')


class VariantCallingMetricsInline(admin.StackedInline):
    model = VariantCallingMetrics
    extra = 0
    can_delete = False
    fields = ('total_variants', 'snp_count', 'indel_count', 'titv_ratio')
    readonly_fields = ('total_variants', 'snp_count', 'indel_count', 'titv_ratio', 'created_at', 'updated_at')


class ExpressionMetricsInline(admin.StackedInline):
    model = ExpressionMetrics
    extra = 0
    can_delete = False
    fields = ('genes_detected', 'mapping_rate_percent', 'normalization_method')
    readonly_fields = ('genes_detected', 'mapping_rate_percent', 'normalization_method', 'created_at', 'updated_at')


# ============================================================================
# CORE ANALYSIS ENTITY
# ============================================================================

class AnalysisAdmin(admin.ModelAdmin):
    list_display = ('analysis_id', 'sequencing_run', 'analysis_type', 'pipeline_name', 'status', 'completed_at')
    list_filter = ('analysis_type', 'pipeline_name', 'status', 'created_at')
    search_fields = ('analysis_id', 'sequencing_run__run_id', 'sample__sample_id')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [QCMetricsInline, AlignmentMetricsInline, VariantCallingMetricsInline, ExpressionMetricsInline]

    fieldsets = (
        ('Analysis Information', {
            'fields': ('analysis_id', 'sequencing_run', 'sample', 'analysis_type')
        }),
        ('Pipeline Details', {
            'fields': ('pipeline_name', 'pipeline_version', 'parameters')
        }),
        ('Execution', {
            'fields': ('status', 'started_at', 'completed_at')
        }),
        ('Documentation', {
            'fields': ('description',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ============================================================================
# ANALYSIS RESULT ENTITIES - READ-ONLY
# ============================================================================

class ReportAdmin(admin.ModelAdmin):
    list_display = ('analysis', 'report_type', 'quality_flag', 'created_at')
    list_filter = ('report_type', 'quality_flag', 'created_at')
    search_fields = ('analysis__analysis_id', 'analysis__sequencing_run__run_id')
    readonly_fields = ('analysis', 'report_type', 'quality_flag', 'metrics', 'created_at', 'updated_at')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class QCMetricsAdmin(admin.ModelAdmin):
    list_display = ('analysis', 'total_sequences', 'gc_content_percent', 'qc_status', 'created_at')
    list_filter = ('qc_status', 'created_at')
    search_fields = ('analysis__analysis_id', 'analysis__sequencing_run__run_id')
    readonly_fields = ('analysis', 'total_sequences', 'gc_content_percent', 'qc_status', 'created_at', 'updated_at')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AlignmentMetricsAdmin(admin.ModelAdmin):
    list_display = ('analysis', 'total_reads', 'mapped_reads', 'mapping_rate_percent', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('analysis__analysis_id', 'analysis__sequencing_run__run_id')
    readonly_fields = ('analysis', 'total_reads', 'mapped_reads', 'mapping_rate_percent', 'created_at', 'updated_at')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class VariantCallingMetricsAdmin(admin.ModelAdmin):
    list_display = ('analysis', 'total_variants', 'snp_count', 'indel_count', 'titv_ratio', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('analysis__analysis_id', 'analysis__sequencing_run__run_id')
    readonly_fields = ('analysis', 'total_variants', 'snp_count', 'indel_count', 'titv_ratio', 'created_at', 'updated_at')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ExpressionMetricsAdmin(admin.ModelAdmin):
    list_display = ('analysis', 'genes_detected', 'mapping_rate_percent', 'normalization_method', 'created_at')
    list_filter = ('normalization_method', 'created_at')
    search_fields = ('analysis__analysis_id', 'analysis__sequencing_run__run_id')
    readonly_fields = ('analysis', 'genes_detected', 'mapping_rate_percent', 'normalization_method', 'created_at', 'updated_at')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# ============================================================================
# Register with custom admin site
# ============================================================================

admin_site.register(Analysis, AnalysisAdmin)
admin_site.register(Report, ReportAdmin)
admin_site.register(QCMetrics, QCMetricsAdmin)
admin_site.register(AlignmentMetrics, AlignmentMetricsAdmin)
admin_site.register(VariantCallingMetrics, VariantCallingMetricsAdmin)
admin_site.register(ExpressionMetrics, ExpressionMetricsAdmin)
