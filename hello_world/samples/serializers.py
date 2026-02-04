"""
DRF serializers for samples app.
"""
from rest_framework import serializers
from .models import Organism, TissueType, Donor, Sample


class OrganismSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organism
        fields = [
            'id', 'scientific_name', 'common_name', 'taxonomy_id',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class TissueTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TissueType
        fields = [
            'id', 'name', 'description', 'ontology_id', 'created_at'
        ]
        read_only_fields = ['created_at']


class DonorSerializer(serializers.ModelSerializer):
    organism_detail = OrganismSerializer(source='organism', read_only=True)
    
    class Meta:
        model = Donor
        fields = [
            'id', 'donor_id', 'organism', 'organism_detail',
            'age', 'sex', 'disease_state', 'genotype', 'phenotype',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class SampleListSerializer(serializers.ModelSerializer):
    donor_id = serializers.CharField(source='donor.donor_id', read_only=True)
    tissue_type_name = serializers.CharField(source='tissue_type.name', read_only=True)
    
    class Meta:
        model = Sample
        fields = [
            'id', 'sample_id', 'donor', 'donor_id', 'tissue_type', 'tissue_type_name',
            'sample_type', 'created_at'
        ]
        read_only_fields = ['created_at']


class SampleDetailSerializer(serializers.ModelSerializer):
    donor_detail = DonorSerializer(source='donor', read_only=True)
    tissue_type_detail = TissueTypeSerializer(source='tissue_type', read_only=True)
    
    class Meta:
        model = Sample
        fields = [
            'id', 'sample_id', 'donor', 'donor_detail', 'tissue_type', 'tissue_type_detail',
            'sample_type', 'collection_date', 'passage_number', 'cell_count', 'viability',
            'storage_conditions', 'description', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
