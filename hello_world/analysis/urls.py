"""
URL routing for analysis app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Import the HTML/listing views first so their URL patterns are checked
# before the DRF router paths. This ensures the "View Metrics/Files"
# link opens the readable HTML page instead of the raw API JSON.
from .views_lists import analysis_list, analyses_for_run, analysis_detail

urlpatterns = [
    path('list/', analysis_list, name='analysis_list'),
    path('runs/<str:run_id>/analyses/', analyses_for_run, name='analyses_for_run'),
    # Detail view uses 'analysis_id' to match view parameter
    path('analyses/<int:analysis_id>/', analysis_detail, name='analysis_detail'),
]


router = DefaultRouter()
from .viewsets import (
    AnalysisViewSet,
    ReportViewSet,
    QCMetricsViewSet,
    AlignmentMetricsViewSet,
    VariantCallingMetricsViewSet,
    ExpressionMetricsViewSet,
)

router.register(r'analyses', AnalysisViewSet, basename='analysis')
router.register(r'reports', ReportViewSet, basename='report')
router.register(r'qc-metrics', QCMetricsViewSet, basename='qc-metrics')
router.register(r'alignment-metrics', AlignmentMetricsViewSet, basename='alignment-metrics')
router.register(r'variant-metrics', VariantCallingMetricsViewSet, basename='variant-metrics')
router.register(r'expression-metrics', ExpressionMetricsViewSet, basename='expression-metrics')

# Include API routes after the HTML/web routes so the web views take precedence
urlpatterns += [
    path('', include(router.urls)),
]
