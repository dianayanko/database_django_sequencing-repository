"""
Custom Django AdminSite configuration for Sequencing Repository.
Provides unified branding and grouping of models by domain.
"""
from django.contrib.admin import AdminSite
from django.apps import apps


class SequencingRepositoryAdminSite(AdminSite):
    """
    Custom admin site for the Sequencing Repository project.
    Groups models by biological/technical domain for improved clarity.
    """
    site_header = "Sequencing Repository Admin"
    site_title = "Sequencing Repository"
    index_title = "Welcome to the Sequencing Repository Management Console"

    def index(self, request, extra_context=None):
        """
        Override index to organize models into logical groups.
        """
        extra_context = extra_context or {}
        
        # Group models by domain
        app_list = super().index(request, extra_context).context_data.get('app_list', [])
        
        # Reorganize app_list for better UX
        organized_apps = []
        
        # Order and group apps
        app_order = [
            'samples',      # Core biological entities
            'sequencing',   # Core sequencing entities  
            'analysis',     # Analysis results
            'files',        # File metadata
        ]
        
        for app_label in app_order:
            for app in app_list:
                if app['app_label'] == app_label:
                    organized_apps.append(app)
                    break
        
        # Add any remaining apps not in our order
        organized_labels = {app['app_label'] for app in organized_apps}
        for app in app_list:
            if app['app_label'] not in organized_labels:
                organized_apps.append(app)
        
        extra_context['app_list'] = organized_apps
        return super().index(request, extra_context)


# Create the singleton instance
admin_site = SequencingRepositoryAdminSite(name='admin')
