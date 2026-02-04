"""
Web views for samples app (non-API).
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Sample
from .forms import SampleForm
from django.db.models import QuerySet


@require_http_methods(["GET"])
def sample_list(request):
    """Display list of all samples."""
    samples = Sample.objects.select_related('donor', 'tissue_type').all()
    context = {
        'samples': samples,
        'title': 'Samples',
    }
    return render(request, 'samples/sample_list.html', context)


@require_http_methods(["GET", "POST"])
def sample_create(request):
    """Create a new sample."""
    if request.method == 'POST':
        form = SampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sample_list')
    else:
        form = SampleForm()
    
    context = {
        'form': form,
        'title': 'Add Sample',
    }
    return render(request, 'samples/sample_form.html', context)


@require_http_methods(["GET"])
def sample_detail(request, pk):
    """Display sample detail."""
    sample = get_object_or_404(Sample, pk=pk)
    context = {
        'sample': sample,
        'title': f'Sample: {sample.sample_id}',
    }
    return render(request, 'samples/sample_detail.html', context)


@require_http_methods(["GET"])
def storage_overview(request):
    """Show samples grouped by storage option."""
    choices = getattr(Sample, 'STORAGE_CHOICES', [])
    groups = []
    for key, label in choices:
        samples = Sample.objects.filter(storage_conditions=key).order_by('-created_at')
        groups.append({'key': key, 'label': label, 'samples': samples})

    context = {
        'groups': groups,
        'title': 'Storage Overview',
    }
    return render(request, 'samples/storage_list.html', context)


@require_http_methods(["GET"])
def sample_report(request, sample_id):
    """
    Display comprehensive report for a single sample including:
    - Sample metadata
    - Donor metadata
    - All SequencingRuns for that sample
    - All Analyses for each run
    - All Files for each run/analysis
    """
    from django.db.models import Prefetch
    from hello_world.sequencing.models import SequencingRun
    from hello_world.analysis.models import Analysis
    from hello_world.files.models import FileAssociation

    # Fetch sample with optimized queries
    sample = get_object_or_404(
        Sample.objects.select_related('donor', 'donor__organism', 'tissue_type'),
        sample_id=sample_id
    )

    # Prefetch sequencing runs with related analyses
    runs_prefetch = Prefetch(
        'sequencing_run_set',
        SequencingRun.objects.select_related('platform', 'project').prefetch_related(
            Prefetch(
                'analysis_set',
                Analysis.objects.select_related(
                    'qc_metrics', 'alignment_metrics', 'variant_metrics', 'expression_metrics'
                ).prefetch_related(
                    'reports',
                    Prefetch(
                        'fileassociation_set',
                        FileAssociation.objects.select_related('file_metadata')
                    )
                )
            )
        )
    )

    # Re-fetch sample with prefetch
    sample = Sample.objects.filter(sample_id=sample_id).prefetch_related(runs_prefetch).first()

    if not sample:
        return get_object_or_404(Sample, sample_id=sample_id)  # Raise 404 if not found

    context = {
        'sample': sample,
        'donor': sample.donor,
        'title': f'Sample Report: {sample.sample_id}',
    }

    return render(request, 'samples/sample_report.html', context)
