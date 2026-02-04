"""
Models for sequencing projects, runs, and platform metadata.
"""
from django.db import models
from hello_world.samples.models import Sample


class SequencingPlatform(models.Model):
    """Represents a sequencing platform/instrument."""
    
    PLATFORM_TYPE_CHOICES = [
        ('illumina', 'Illumina'),
        ('ont', 'Oxford Nanopore Technologies'),
        ('pacbio', 'PacBio'),
        ('ion_torrent', 'Ion Torrent'),
        ('bgiseq', 'BGI-SEQ'),
        ('element', 'Element Biosciences'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=255, unique=True)
    platform_type = models.CharField(max_length=50, choices=PLATFORM_TYPE_CHOICES)
    manufacturer = models.CharField(max_length=255)
    instrument_model = models.CharField(max_length=255, blank=True)
    read_length_min = models.IntegerField(null=True, blank=True)
    read_length_max = models.IntegerField(null=True, blank=True)
    read_type = models.CharField(
        max_length=50,
        choices=[('single', 'Single-end'), ('paired', 'Paired-end'), ('long', 'Long-read')],
        default='paired'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class SequencingProject(models.Model):
    """Represents a sequencing project containing one or more samples."""
    
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('sequencing', 'Sequencing'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]
    
    project_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    
    # Project details
    pi_name = models.CharField(max_length=255, blank=True, help_text="Principal Investigator")
    institution = models.CharField(max_length=255, blank=True)
    project_type = models.CharField(
        max_length=50,
        choices=[('rna_seq', 'RNA-seq'), ('wes', 'Whole Exome Seq'), ('wgs', 'Whole Genome Seq'), ('mixed', 'Mixed')],
        default='rna_seq'
    )
    
    # Status and timeline
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='planning')
    start_date = models.DateField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    
    # Relationships
    samples = models.ManyToManyField(Sample, related_name='sequencing_projects')
    
    # Documentation
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.project_id}: {self.title}"


class LibraryPreparation(models.Model):
    """Metadata about library preparation for sequencing."""
    
    LIBRARY_KIT_CHOICES = [
        ('truseq_stranded_mrna', 'TruSeq Stranded mRNA'),
        ('truseq_rna', 'TruSeq RNA'),
        ('nextera_xt', 'Nextera XT'),
        ('nextera_dna_flex', 'Nextera DNA Flex'),
        ('agilent_sureselect', 'Agilent SureSelect'),
        ('roche_nimbleseq', 'Roche NimbleSeq'),
        ('10x_chromium', '10x Chromium'),
        ('bd_rhapsody', 'BD Rhapsody'),
        ('other', 'Other'),
    ]
    
    library_id = models.CharField(max_length=255, unique=True)
    library_kit = models.CharField(max_length=100, choices=LIBRARY_KIT_CHOICES)
    
    # Library characteristics
    insert_size_bp = models.IntegerField(null=True, blank=True)
    fragment_size_bp = models.IntegerField(null=True, blank=True)
    library_concentration = models.FloatField(null=True, blank=True, help_text="ng/µL")
    library_volume_ul = models.FloatField(null=True, blank=True)
    
    # QC metrics
    qc_status = models.CharField(
        max_length=50,
        choices=[('pass', 'Pass'), ('fail', 'Fail'), ('pending', 'Pending')],
        default='pending'
    )
    rna_integrity_number = models.FloatField(null=True, blank=True, help_text="RIN score")
    dna_integrity = models.CharField(max_length=100, blank=True)
    
    # Preparation details
    prep_date = models.DateField(null=True, blank=True)
    technician = models.CharField(max_length=255, blank=True)
    
    # Indexing
    index_name = models.CharField(max_length=100, blank=True)
    index_sequence = models.CharField(max_length=100, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.library_id


class SequencingRun(models.Model):
    """Represents a single sequencing run that sequences one or more samples."""
    
    RUN_STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('archived', 'Archived'),
    ]
    
    run_id = models.CharField(max_length=255, unique=True)
    project = models.ForeignKey(SequencingProject, on_delete=models.CASCADE, related_name='sequencing_runs')
    platform = models.ForeignKey(SequencingPlatform, on_delete=models.SET_NULL, null=True, related_name='runs')
    
    # Sample and library relationship
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='sequencing_runs')
    library_preparation = models.ForeignKey(
        LibraryPreparation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sequencing_runs'
    )
    
    # Run details
    run_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=RUN_STATUS_CHOICES, default='planned')
    flowcell_id = models.CharField(max_length=255, blank=True)
    
    # Sequencing parameters
    total_reads = models.BigIntegerField(null=True, blank=True)
    total_bases = models.BigIntegerField(null=True, blank=True)
    q30_percentage = models.FloatField(null=True, blank=True, help_text="Percentage of bases with Q>=30")
    mean_read_length = models.IntegerField(null=True, blank=True)
    
    # Run outcome
    completion_date = models.DateField(null=True, blank=True)
    technician = models.CharField(max_length=255, blank=True)
    
    # Documentation
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-run_date', '-created_at']
        unique_together = [['project', 'run_id']]
    
    def __str__(self):
        return f"{self.run_id} ({self.sample.sample_id})"
