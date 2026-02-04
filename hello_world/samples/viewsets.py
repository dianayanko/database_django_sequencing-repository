"""
DRF viewsets for samples app.
"""
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Organism, TissueType, Donor, Sample
from .serializers import (
    OrganismSerializer,
    TissueTypeSerializer,
    DonorSerializer,
    SampleListSerializer,
    SampleDetailSerializer,
)


class OrganismViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing organisms.
    """
    queryset = Organism.objects.all()
    serializer_class = OrganismSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['scientific_name', 'common_name', 'taxonomy_id']
    ordering_fields = ['scientific_name', 'created_at']
    ordering = ['scientific_name']


class TissueTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing tissue types.
    """
    queryset = TissueType.objects.all()
    serializer_class = TissueTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'ontology_id']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class DonorViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing donors.
    """
    queryset = Donor.objects.select_related('organism').all()
    serializer_class = DonorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['organism', 'sex', 'disease_state']
    search_fields = ['donor_id', 'organism__scientific_name']
    ordering_fields = ['donor_id', 'created_at']
    ordering = ['donor_id']


class SampleViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing biological samples.
    """
    queryset = Sample.objects.select_related('donor', 'tissue_type').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['donor', 'tissue_type', 'sample_type']
    search_fields = ['sample_id', 'donor__donor_id']
    ordering_fields = ['sample_id', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SampleDetailSerializer
        return SampleListSerializer
