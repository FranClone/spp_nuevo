"""
Web Server Gateway Interface: describe como un servidor web debe comunicarse con aplicaciones web escritas en python
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SPP_Django.settings')

application = get_wsgi_application()
