"""
Web views for sequencing app (non-API).
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from hello_world.samples.models import Sample
from .forms import SequencingRunForm
from django.shortcuts import render, get_object_or_404
from .models import SequencingProject

def project_detail_view(request, project_id):
    # Pobranie projektu po project_id
    project = get_object_or_404(SequencingProject, project_id=project_id)
    
    # Pobranie powiązanych próbek
    samples = project.samples.all()
    
    return render(request, 'sequencing/project_detail.html', {
        'project': project,
        'samples': samples
    })


@require_http_methods(["GET", "POST"])
def sequencing_run_create_for_sample(request, sample_id):
    """Create a SequencingRun linked to a Sample identified by sample_id."""
    sample = get_object_or_404(Sample, sample_id=sample_id)

    if request.method == 'POST':
        form = SequencingRunForm(request.POST)
        if form.is_valid():
            run = form.save(commit=False)
            run.sample = sample
            run.save()
            return redirect('sample_detail', pk=sample.pk)
    else:
        form = SequencingRunForm()

    context = {
        'form': form,
        'sample': sample,
        'title': f'Add Run for {sample.sample_id}',
    }
    return render(request, 'sequencing/run_form.html', context)
