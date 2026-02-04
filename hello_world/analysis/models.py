"""
Models for bioinformatics analyses and quality control reports.
"""
from django.db import models
from hello_world.sequencing.models import SequencingRun
from hello_world.samples.models import Sample


class Analysis(models.Model):
    """Represents a bioinformatics analysis performed on sequencing data."""
    
    ANALYSIS_TYPE_CHOICES = [
        ('qc', 'Quality Control'),
        ('alignment', 'Read Alignment'),
        ('variant_calling', 'Variant Calling'),
        ('expression', 'Expression Analysis'),
        ('abundance', 'Abundance Estimation'),
        ('cnv', 'Copy Number Variation'),
        ('custom', 'Custom Analysis'),
    ]
    
    PIPELINE_CHOICES = [
        ('fastqc', 'FastQC'),
        ('multiqc', 'MultiQC'),
        ('bwa', 'BWA'),
        ('bowtie2', 'Bowtie2'),
        ('star', 'STAR'),
        ('salmon', 'Salmon'),
        ('kallisto', 'Kallisto'),
        ('samtools', 'SAMtools'),
        ('bcftools', 'BCFtools'),
        ('freebayes', 'FreeBayes'),
        ('gatk', 'GATK'),
        ('deepvariant', 'DeepVariant'),
        ('other', 'Other'),
    ]
    
    analysis_id = models.CharField(max_length=255, unique=True)
    sequencing_run = models.ForeignKey(SequencingRun, on_delete=models.CASCADE, related_name='analyses')
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='analyses', null=True, blank=True)
    
    # Analysis details
    analysis_type = models.CharField(max_length=50, choices=ANALYSIS_TYPE_CHOICES)
    pipeline_name = models.CharField(max_length=100, choices=PIPELINE_CHOICES)
    pipeline_version = models.CharField(max_length=100, blank=True)
    
    # Execution
    status = models.CharField(
        max_length=50,
        choices=[('queued', 'Queued'), ('running', 'Running'), ('completed', 'Completed'), ('failed', 'Failed')],
        default='queued'
    )
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Parameters (stored as JSON string)
    parameters = models.JSONField(default=dict, blank=True)
    
    # Documentation
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.analysis_id} ({self.get_analysis_type_display()})"


class Report(models.Model):
    """Base report model for analysis results and metrics."""
    
    REPORT_TYPE_CHOICES = [
        ('qc', 'QC Report'),
        ('alignment', 'Alignment Report'),
        ('variant', 'Variant Calling Report'),
        ('expression', 'Expression Report'),
        ('abundance', 'Abundance Report'),
        ('cnv', 'CNV Report'),
    ]
    
    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=50, choices=REPORT_TYPE_CHOICES)
    
    # Report content
    summary = models.TextField(blank=True)
    metrics = models.JSONField(default=dict, blank=True)
    
    # File references
    report_url = models.CharField(max_length=500, blank=True)
    output_directory = models.CharField(max_length=500, blank=True)
    
    # Status
    quality_flag = models.CharField(
        max_length=50,
        choices=[('pass', 'Pass'), ('warn', 'Warning'), ('fail', 'Fail')],
        default='pass'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_report_type_display()} - {self.analysis.analysis_id}"


class QCMetrics(models.Model):
    """Quality control metrics from FastQC or MultiQC."""
    
    analysis = models.OneToOneField(
        Analysis,
        on_delete=models.CASCADE,
        related_name='qc_metrics',
        limit_choices_to={'analysis_type': 'qc'}
    )
    
    # Read metrics
    total_sequences = models.BigIntegerField(null=True, blank=True)
    gc_content_percent = models.FloatField(null=True, blank=True)
    n_content_percent = models.FloatField(null=True, blank=True)
    
    # Quality metrics
    mean_quality_score = models.FloatField(null=True, blank=True)
    percentage_q30 = models.FloatField(null=True, blank=True)
    percentage_q20 = models.FloatField(null=True, blank=True)
    
    # Duplication metrics
    percent_duplicates = models.FloatField(null=True, blank=True)
    
    # Adapter content
    adapter_content_percent = models.FloatField(null=True, blank=True)
    
    # Status
    qc_status = models.CharField(
        max_length=50,
        choices=[('pass', 'Pass'), ('warn', 'Warning'), ('fail', 'Fail')],
        default='pass'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"QC Metrics - {self.analysis.analysis_id}"


class AlignmentMetrics(models.Model):
    """Alignment statistics from BWA, STAR, or similar aligners."""
    
    analysis = models.OneToOneField(
        Analysis,
        on_delete=models.CASCADE,
        related_name='alignment_metrics',
        limit_choices_to={'analysis_type': 'alignment'}
    )
    
    # Alignment statistics
    total_reads = models.BigIntegerField(null=True, blank=True)
    mapped_reads = models.BigIntegerField(null=True, blank=True)
    unmapped_reads = models.BigIntegerField(null=True, blank=True)
    mapping_rate_percent = models.FloatField(null=True, blank=True)
    
    # Read quality
    properly_paired_percent = models.FloatField(null=True, blank=True)
    median_insert_size = models.IntegerField(null=True, blank=True)
    
    # Duplication
    percent_duplicates = models.FloatField(null=True, blank=True)
    
    # Coverage metrics
    mean_coverage = models.FloatField(null=True, blank=True)
    coverage_uniformity = models.FloatField(null=True, blank=True, help_text="Gini coefficient or similar")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Alignment Metrics - {self.analysis.analysis_id}"


class VariantCallingMetrics(models.Model):
    """Metrics from variant calling pipelines (GATK, FreeBayes, DeepVariant)."""
    
    analysis = models.OneToOneField(
        Analysis,
        on_delete=models.CASCADE,
        related_name='variant_metrics',
        limit_choices_to={'analysis_type': 'variant_calling'}
    )
    
    # Variant counts
    total_variants = models.BigIntegerField(null=True, blank=True)
    snp_count = models.BigIntegerField(null=True, blank=True)
    indel_count = models.BigIntegerField(null=True, blank=True)
    multi_allelic_count = models.BigIntegerField(null=True, blank=True)
    
    # Quality metrics
    mean_variant_quality = models.FloatField(null=True, blank=True)
    percent_variants_pass_filter = models.FloatField(null=True, blank=True)
    
    # Transition/transversion ratio
    titv_ratio = models.FloatField(null=True, blank=True)
    
    # Functional impact (if annotated)
    percent_missense = models.FloatField(null=True, blank=True)
    percent_synonymous = models.FloatField(null=True, blank=True)
    percent_frameshift = models.FloatField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Variant Metrics - {self.analysis.analysis_id}"


class ExpressionMetrics(models.Model):
    """Gene expression metrics from RNA-seq analysis."""
    
    analysis = models.OneToOneField(
        Analysis,
        on_delete=models.CASCADE,
        related_name='expression_metrics',
        limit_choices_to={'analysis_type': 'expression'}
    )
    
    # Expression statistics
    genes_detected = models.IntegerField(null=True, blank=True, help_text="Number of genes with non-zero counts")
    total_gene_count = models.IntegerField(null=True, blank=True, help_text="Reference genome gene count")
    
    # Quality metrics
    mapping_rate_percent = models.FloatField(null=True, blank=True)
    percent_mtdna = models.FloatField(null=True, blank=True)
    percent_rrna = models.FloatField(null=True, blank=True)
    
    # Normalization
    normalization_method = models.CharField(
        max_length=100,
        choices=[('cpm', 'CPM'), ('tpm', 'TPM'), ('rpkm', 'RPKM'), ('deseq2', 'DESeq2'), ('other', 'Other')],
        blank=True
    )
    
    # Statistics
    mean_gene_expression = models.FloatField(null=True, blank=True)
    median_gene_expression = models.FloatField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Expression Metrics - {self.analysis.analysis_id}"
