"""
DRF viewsets for analysis app.
"""
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Analysis, Report, QCMetrics, AlignmentMetrics, VariantCallingMetrics, ExpressionMetrics
from .serializers import (
    AnalysisListSerializer,
    AnalysisDetailSerializer,
    ReportSerializer,
    QCMetricsSerializer,
    AlignmentMetricsSerializer,
    VariantCallingMetricsSerializer,
    ExpressionMetricsSerializer,
)


class AnalysisViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing analyses.
    """
    queryset = Analysis.objects.select_related('sequencing_run', 'sample').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sequencing_run', 'sample', 'analysis_type', 'pipeline_name', 'status']
    search_fields = ['analysis_id', 'sequencing_run__run_id']
    ordering_fields = ['analysis_id', 'created_at', 'status']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AnalysisDetailSerializer
        return AnalysisListSerializer


class ReportViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing reports.
    """
    queryset = Report.objects.select_related('analysis').all()
    serializer_class = ReportSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['analysis', 'report_type', 'quality_flag']
    search_fields = ['analysis__analysis_id']
    ordering_fields = ['created_at', 'quality_flag']
    ordering = ['-created_at']


class QCMetricsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing QC metrics.
    """
    queryset = QCMetrics.objects.select_related('analysis').all()
    serializer_class = QCMetricsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['analysis', 'qc_status']
    ordering_fields = ['created_at', 'percentage_q30']
    ordering = ['-created_at']


class AlignmentMetricsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing alignment metrics.
    """
    queryset = AlignmentMetrics.objects.select_related('analysis').all()
    serializer_class = AlignmentMetricsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['analysis']
    ordering_fields = ['created_at', 'mapping_rate_percent']
    ordering = ['-created_at']


class VariantCallingMetricsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing variant calling metrics.
    """
    queryset = VariantCallingMetrics.objects.select_related('analysis').all()
    serializer_class = VariantCallingMetricsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['analysis']
    ordering_fields = ['created_at', 'total_variants', 'titv_ratio']
    ordering = ['-created_at']


class ExpressionMetricsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing expression metrics.
    """
    queryset = ExpressionMetrics.objects.select_related('analysis').all()
    serializer_class = ExpressionMetricsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['analysis', 'normalization_method']
    ordering_fields = ['created_at', 'genes_detected']
    ordering = ['-created_at']
