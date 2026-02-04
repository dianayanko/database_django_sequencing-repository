"""
URL configuration for hello_world project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
#from rest_framework.documentation import include_docs_urls

from hello_world.core import views as core_views
from hello_world.admin_site import admin_site

urlpatterns = [
    path("", core_views.index, name='dashboard'),
    path("admin/", admin_site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    # Web routes
    path("samples/", include("hello_world.samples.urls")),
    # API endpoints
    path("api/", include("rest_framework.urls")),
    #path("api/docs/", include_docs_urls(title="Sequencing Repository API")),
    path("api/samples/", include("hello_world.samples.urls")),
    path("api/sequencing/", include("hello_world.sequencing.urls")),
    path("api/analysis/", include("hello_world.analysis.urls")),
    path("api/files/", include("hello_world.files.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
