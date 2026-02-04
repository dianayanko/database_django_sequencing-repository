"""
DRF serializers for sequencing app.
"""
from rest_framework import serializers
from .models import SequencingPlatform, SequencingProject, LibraryPreparation, SequencingRun


class SequencingPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = SequencingPlatform
        fields = [
            'id', 'name', 'platform_type', 'manufacturer', 'instrument_model',
            'read_length_min', 'read_length_max', 'read_type',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class LibraryPreparationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryPreparation
        fields = [
            'id', 'library_id', 'library_kit', 'insert_size_bp', 'fragment_size_bp',
            'library_concentration', 'library_volume_ul', 'qc_status',
            'rna_integrity_number', 'dna_integrity', 'prep_date', 'technician',
            'index_name', 'index_sequence', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class SequencingProjectListSerializer(serializers.ModelSerializer):
    sample_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SequencingProject
        fields = [
            'id', 'project_id', 'title', 'project_type', 'status',
            'pi_name', 'sample_count', 'created_at'
        ]
        read_only_fields = ['created_at']
    
    def get_sample_count(self, obj):
        return obj.samples.count()


class SequencingProjectDetailSerializer(serializers.ModelSerializer):
    samples_detail = serializers.SerializerMethodField()
    
    class Meta:
        model = SequencingProject
        fields = [
            'id', 'project_id', 'title', 'description', 'pi_name', 'institution',
            'project_type', 'status', 'start_date', 'completion_date',
            'samples', 'samples_detail', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_samples_detail(self, obj):
        from hello_world.samples.serializers import SampleListSerializer
        return SampleListSerializer(obj.samples.all(), many=True).data


class SequencingRunListSerializer(serializers.ModelSerializer):
    sample_id = serializers.CharField(source='sample.sample_id', read_only=True)
    platform_name = serializers.CharField(source='platform.name', read_only=True)
    
    class Meta:
        model = SequencingRun
        fields = [
            'id', 'run_id', 'project', 'sample', 'sample_id', 'platform', 'platform_name',
            'status', 'run_date', 'created_at'
        ]
        read_only_fields = ['created_at']


class SequencingRunDetailSerializer(serializers.ModelSerializer):
    sample_detail = serializers.SerializerMethodField()
    platform_detail = SequencingPlatformSerializer(source='platform', read_only=True)
    library_preparation_detail = LibraryPreparationSerializer(source='library_preparation', read_only=True)
    
    class Meta:
        model = SequencingRun
        fields = [
            'id', 'run_id', 'project', 'platform', 'platform_detail', 'sample', 'sample_detail',
            'library_preparation', 'library_preparation_detail', 'run_date', 'status',
            'flowcell_id', 'total_reads', 'total_bases', 'q30_percentage', 'mean_read_length',
            'completion_date', 'technician', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_sample_detail(self, obj):
        from hello_world.samples.serializers import SampleDetailSerializer
        return SampleDetailSerializer(obj.sample, read_only=True).data
