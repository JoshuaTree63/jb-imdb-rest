
import os

import django
from Tools.i18n.makelocalealias import pprint

os.environ["DJANGO_SETTINGS_MODULE"] = "imdb_rest.settings"
django.setup()
from imdb_app.models import *


# movies = Movie.object.filter(year__gte=2000)
# print(movies)

actor = Actor.objects.all()
print(actor)

