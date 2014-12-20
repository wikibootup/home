import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'seeseehome.settings'

path = '/home/seebuntu/github/home/seeseehome'
if path not in sys.path:
      sys.path.append(path)

from django.core.wsgi import get_wsgi_application
from dj_static import Cling
application = Cling(get_wsgi_application())

