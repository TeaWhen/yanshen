import os
import sys

path = '/home/mrx/yanshen'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'yanshen.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
