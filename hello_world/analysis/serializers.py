"""
DRF serializers for analysis app.
"""
from rest_framework import serializers
from .models import (
    Analysis,
    Report,
    QCMetrics,
    AlignmentMetrics,
    VariantCallingMetrics,
    ExpressionMetrics,
)


class QCMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QCMetrics
        fields = [
            'id', 'analysis', 'total_sequences', 'gc_content_percent', 'n_content_percent',
            'mean_quality_score', 'percentage_q30', 'percentage_q20', 'percent_duplicates',
            'adapter_content_percent', 'qc_status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class AlignmentMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlignmentMetrics
        fields = [
            'id', 'analysis', 'total_reads', 'mapped_reads', 'unmapped_reads',
            'mapping_rate_percent', 'properly_paired_percent', 'median_insert_size',
            'percent_duplicates', 'mean_coverage', 'coverage_uniformity',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class VariantCallingMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantCallingMetrics
        fields = [
            'id', 'analysis', 'total_variants', 'snp_count', 'indel_count',
            'multi_allelic_count', 'mean_variant_quality', 'percent_variants_pass_filter',
            'titv_ratio', 'percent_missense', 'percent_synonymous', 'percent_frameshift',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ExpressionMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpressionMetrics
        fields = [
            'id', 'analysis', 'genes_detected', 'total_gene_count', 'mapping_rate_percent',
            'percent_mtdna', 'percent_rrna', 'normalization_method',
            'mean_gene_expression', 'median_gene_expression', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            'id', 'analysis', 'report_type', 'summary', 'metrics',
            'report_url', 'output_directory', 'quality_flag',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class AnalysisListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = [
            'id', 'analysis_id', 'sequencing_run', 'analysis_type', 'pipeline_name',
            'status', 'created_at'
        ]
        read_only_fields = ['created_at']


class AnalysisDetailSerializer(serializers.ModelSerializer):
    qc_metrics = QCMetricsSerializer(read_only=True)
    alignment_metrics = AlignmentMetricsSerializer(read_only=True)
    variant_metrics = VariantCallingMetricsSerializer(read_only=True)
    expression_metrics = ExpressionMetricsSerializer(read_only=True)
    reports = ReportSerializer(many=True, read_only=True)
    
    class Meta:
        model = Analysis
        fields = [
            'id', 'analysis_id', 'sequencing_run', 'sample', 'analysis_type',
            'pipeline_name', 'pipeline_version', 'status', 'started_at', 'completed_at',
            'parameters', 'description', 'notes', 'qc_metrics', 'alignment_metrics',
            'variant_metrics', 'expression_metrics', 'reports',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
