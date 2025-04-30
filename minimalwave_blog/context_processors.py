from datetime import datetime
from django.conf import settings
from django.utils import timezone
from django.conf import settings

def common_context(request):
    """
    Context processor to add common variables to all templates
    """
    return {
        'site_name': 'Minimal Wave Blog',
        'site_description': 'A personal blog with minimal wave aesthetics',
        'site_url': request.build_absolute_uri('/').rstrip('/'),
        'current_year': settings.USE_TZ and timezone.now().year or datetime.datetime.now().year,
    }
