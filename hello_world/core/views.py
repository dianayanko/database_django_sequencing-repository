from django.shortcuts import render
from hello_world.samples.models import Sample

def index(request):
    # Fetch real database statistics
    total_samples = Sample.objects.count()
    recent_samples = Sample.objects.all().order_by('-created_at')[:5]
    latest_sample = Sample.objects.all().order_by('-created_at').first()
    
    context = {
        "title": "Django example",
        "total_samples": total_samples,
        "recent_samples": recent_samples,
        "latest_sample": latest_sample,
    }
    return render(request, "index.html", context)
