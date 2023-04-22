"""imdb_rest URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from rest_framework.routers import DefaultRouter

from imdb_app import views
from imdb_app.view_sets import MovieViewSet

# http://127.0.0.1:8000/api/imdb/movies
# movies

# http://127.0.0.1:8000/api/imdb/movies/3
# http://127.0.0.1:8000/api/imdb/movies/327

router = DefaultRouter()
router.register('movies', MovieViewSet)
router.register('actors', MovieViewSet)

urlpatterns = [
    path('movies/<int:movie_id>/actors/<int:actor_id>', views.movie_actor),

    # path('movies', views.get_movies),
    # path('movies/<int:movie_id>', views.get_movie),


    path('movies/<int:movie_id>/actors', views.get_movie_actors),
    path('ratings', views.get_ratings),
    path('movies/<int:movie_id>/ratings', views.movie_ratings),
    path('movies/<int:movie_id>/ratings/avg', views.get_avg_movie_rating),
    path('actors', views.get_actors),
    path('actors/<int:actor_id>', views.get_actor),
    path('movies/<int:movie_id>/actors', views.movie_actors),
    path('movies/<int:movie_id>/ratings', views.movie_ratings),
    path('movies/<int:movie_id>/ratings/<int:rating_id>', views.movie_rating),
    path('actors', views.actors)
]

urlpatterns.extend(router.urls)

