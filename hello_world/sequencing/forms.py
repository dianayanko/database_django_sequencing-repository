"""
Forms for sequencing app (web forms).
"""
from django import forms
from .models import SequencingRun


class SequencingRunForm(forms.ModelForm):
    class Meta:
        model = SequencingRun
        # exclude sample; it will be set by the view based on sample_id
        fields = [
            'run_id',
            'project',
            'platform',
            'library_preparation',
            'run_date',
            'status',
            'flowcell_id',
            'total_reads',
            'total_bases',
            'q30_percentage',
            'mean_read_length',
            'completion_date',
            'technician',
            'notes',
        ]
        widgets = {
            'run_date': forms.DateInput(attrs={'type': 'date'}),
            'completion_date': forms.DateInput(attrs={'type': 'date'}),
        }
