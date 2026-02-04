"""
DRF serializers for files app.
"""
from rest_framework import serializers
from .models import FileMetadata, FileAssociation


class FileMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileMetadata
        fields = [
            'id', 'file_id', 'file_path', 'file_type', 'read_type',
            'file_size_bytes', 'file_format_version', 'total_reads',
            'checksum_md5', 'checksum_sha256', 'is_compressed', 'compression_format',
            'index_file_path', 'storage_location', 'description', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class FileAssociationListSerializer(serializers.ModelSerializer):
    file_metadata_detail = FileMetadataSerializer(source='file_metadata', read_only=True)
    run_id = serializers.CharField(source='sequencing_run.run_id', read_only=True, allow_null=True)
    analysis_id = serializers.CharField(source='analysis.analysis_id', read_only=True, allow_null=True)
    
    class Meta:
        model = FileAssociation
        fields = [
            'id', 'file_metadata', 'file_metadata_detail', 'sequencing_run', 'run_id',
            'analysis', 'analysis_id', 'file_role', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class FileAssociationDetailSerializer(serializers.ModelSerializer):
    file_metadata_detail = FileMetadataSerializer(source='file_metadata', read_only=True)
    
    class Meta:
        model = FileAssociation
        fields = [
            'id', 'file_metadata', 'file_metadata_detail', 'sequencing_run', 'analysis',
            'file_role', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
