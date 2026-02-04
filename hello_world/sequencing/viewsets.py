"""
DRF viewsets for sequencing app.
"""
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import SequencingPlatform, SequencingProject, LibraryPreparation, SequencingRun
from .serializers import (
    SequencingPlatformSerializer,
    SequencingProjectListSerializer,
    SequencingProjectDetailSerializer,
    LibraryPreparationSerializer,
    SequencingRunListSerializer,
    SequencingRunDetailSerializer,
)


class SequencingPlatformViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing sequencing platforms.
    """
    queryset = SequencingPlatform.objects.all()
    serializer_class = SequencingPlatformSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['platform_type', 'read_type']
    search_fields = ['name', 'manufacturer', 'instrument_model']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class LibraryPreparationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing library preparations.
    """
    queryset = LibraryPreparation.objects.all()
    serializer_class = LibraryPreparationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['library_kit', 'qc_status']
    search_fields = ['library_id', 'index_name']
    ordering_fields = ['library_id', 'prep_date', 'created_at']
    ordering = ['-prep_date']


class SequencingProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing sequencing projects.
    """
    queryset = SequencingProject.objects.prefetch_related('samples').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['project_type', 'status']
    search_fields = ['project_id', 'title', 'pi_name']
    ordering_fields = ['project_id', 'created_at', 'start_date']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SequencingProjectDetailSerializer
        return SequencingProjectListSerializer


class SequencingRunViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing sequencing runs.
    """
    queryset = SequencingRun.objects.select_related(
        'project', 'sample', 'platform', 'library_preparation'
    ).all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['project', 'sample', 'platform', 'status']
    search_fields = ['run_id', 'sample__sample_id', 'flowcell_id']
    ordering_fields = ['run_id', 'run_date', 'created_at']
    ordering = ['-run_date', '-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SequencingRunDetailSerializer
        return SequencingRunListSerializer
