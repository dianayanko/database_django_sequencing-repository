"""
Models for tracking sequence data files without storing raw binary data.
"""
from django.db import models
from hello_world.sequencing.models import SequencingRun
from hello_world.analysis.models import Analysis


class FileMetadata(models.Model):
    """Metadata for sequence data files (FASTQ, BAM, VCF) without storing raw binary."""
    
    FILE_TYPE_CHOICES = [
        ('fastq', 'FASTQ'),
        ('fastq_gz', 'FASTQ (gzipped)'),
        ('bam', 'BAM'),
        ('bam_bai', 'BAM Index'),
        ('vcf', 'VCF'),
        ('vcf_gz', 'VCF (gzipped)'),
        ('vcf_tbi', 'VCF Index'),
        ('gff', 'GFF'),
        ('gtf', 'GTF'),
        ('bed', 'BED'),
        ('fasta', 'FASTA'),
        ('fastasta_fai', 'FASTA Index'),
        ('txt', 'Text'),
        ('json', 'JSON'),
        ('csv', 'CSV'),
        ('tsv', 'TSV'),
        ('html', 'HTML'),
        ('pdf', 'PDF'),
        ('other', 'Other'),
    ]
    
    READ_TYPE_CHOICES = [
        ('R1', 'Read 1 (forward)'),
        ('R2', 'Read 2 (reverse)'),
        ('R3', 'Read 3 (index)'),
        ('R4', 'Read 4'),
        ('single', 'Single-end read'),
        ('other', 'Other'),
    ]
    
    file_id = models.CharField(max_length=255, unique=True)
    file_path = models.CharField(max_length=1000, help_text="Full path or URI to file")
    file_type = models.CharField(max_length=50, choices=FILE_TYPE_CHOICES)
    
    # File characteristics
    file_size_bytes = models.BigIntegerField(null=True, blank=True)
    file_format_version = models.CharField(max_length=100, blank=True)
    
    # Read-level metadata
    read_type = models.CharField(max_length=50, choices=READ_TYPE_CHOICES, blank=True)
    total_reads = models.BigIntegerField(null=True, blank=True)
    
    # Data integrity
    checksum_md5 = models.CharField(max_length=32, blank=True)
    checksum_sha256 = models.CharField(max_length=64, blank=True)
    
    # Compression info
    is_compressed = models.BooleanField(default=False)
    compression_format = models.CharField(max_length=50, blank=True, choices=[('gzip', 'gzip'), ('bzip2', 'bzip2'), ('xz', 'xz')])
    
    # Index files
    index_file_path = models.CharField(max_length=1000, blank=True, help_text="Path to BAI, CSI, TBI, etc.")
    
    # Location
    storage_location = models.CharField(
        max_length=50,
        choices=[('local', 'Local filesystem'), ('s3', 'AWS S3'), ('gcs', 'Google Cloud Storage'), ('other', 'Other')],
        default='local'
    )
    
    # Metadata
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.file_id} ({self.get_file_type_display()})"


class FileAssociation(models.Model):
    """
    Associates files with sequencing runs or analyses.
    Enables tracking which files belong to which runs/analyses without duplication.
    """
    
    file_metadata = models.ForeignKey(FileMetadata, on_delete=models.CASCADE, related_name='associations')
    
    # Source (can be associated with run or analysis, but at least one must be set)
    sequencing_run = models.ForeignKey(
        SequencingRun,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='file_associations'
    )
    analysis = models.ForeignKey(
        Analysis,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='file_associations'
    )
    
    # File role
    file_role = models.CharField(
        max_length=100,
        choices=[
            ('raw_reads', 'Raw sequencing reads'),
            ('trimmed_reads', 'Trimmed reads'),
            ('aligned_reads', 'Aligned reads'),
            ('variants', 'Variant calls'),
            ('expression_matrix', 'Expression matrix'),
            ('qc_report', 'QC report'),
            ('alignment_report', 'Alignment report'),
            ('variant_report', 'Variant report'),
            ('supplementary', 'Supplementary file'),
            ('other', 'Other'),
        ],
        blank=True
    )
    
    # Relationship metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = [['file_metadata', 'sequencing_run', 'analysis']]
    
    def clean(self):
        """Ensure at least one of sequencing_run or analysis is set."""
        from django.core.exceptions import ValidationError
        if not self.sequencing_run and not self.analysis:
            raise ValidationError("Either sequencing_run or analysis must be specified.")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        source = self.sequencing_run.run_id if self.sequencing_run else self.analysis.analysis_id
        return f"{self.file_metadata.file_id} → {source}"
