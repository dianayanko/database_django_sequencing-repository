"""
DRF viewsets for files app.
"""
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import FileMetadata, FileAssociation
from .serializers import (
    FileMetadataSerializer,
    FileAssociationListSerializer,
    FileAssociationDetailSerializer,
)


class FileMetadataViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing file metadata.
    """
    queryset = FileMetadata.objects.all()
    serializer_class = FileMetadataSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['file_type', 'read_type', 'storage_location', 'is_compressed']
    search_fields = ['file_id', 'file_path', 'checksum_md5', 'checksum_sha256']
    ordering_fields = ['file_id', 'created_at', 'file_size_bytes']
    ordering = ['-created_at']


class FileAssociationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing file associations with runs and analyses.
    """
    queryset = FileAssociation.objects.select_related(
        'file_metadata', 'sequencing_run', 'analysis'
    ).all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['file_metadata', 'sequencing_run', 'analysis', 'file_role']
    search_fields = ['file_metadata__file_id', 'sequencing_run__run_id', 'analysis__analysis_id']
    ordering_fields = ['created_at', 'file_role']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FileAssociationDetailSerializer
        return FileAssociationListSerializer
