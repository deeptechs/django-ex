"""
WSGI config for PhotoGenius project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# Production ortamı için farklı bir dosya belirledim, wsgi sunucu bunu kullanacak
sys.path.append('src')  # Konsoldan proje dizininden çağırırken burayı path e ekliyorum, PhotoGenius modül okunsun diye.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PhotoGenius.settings.production")

application = get_wsgi_application()
