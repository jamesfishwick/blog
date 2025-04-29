"""
Settings module initialization
"""
import os

# Default to development settings
DJANGO_SETTINGS_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE', 'minimalwave_blog.settings.development')

if DJANGO_SETTINGS_MODULE == 'minimalwave_blog.settings.production':
    from .production import *
else:
    from .development import *
