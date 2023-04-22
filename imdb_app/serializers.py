from django.core.validators import MinValueValidator
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from imdb_app.models import Movie, Actor, MovieActor, Rating
from imdb_app.validators import MinAgeValidator


# class MovieSerializer(serializers.Serializer):
#     name = serializers.CharField()
#     release_year = serializers.IntegerField()
#     description = serializers.CharField()


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        # fields = '__all__'
        fields = ['id', 'name', 'release_year', 'duration_in_min', 'pic_url']
        # exclude = ['pic_url']
        # depth = 1


class DetailedMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        exclude = ['actors']


class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = '__all__'
        # extra_kwargs = {
        #     'birth_year': {
        #         'required': False,
        #         'validators': [MinAgeValidator(5)]
        #     },
        # }


class CastSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieActor
        # fields = '__all__'
        exclude = ['id', 'movie']
        depth = 1


class WriteCastSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieActor
        fields = '__all__'
        # Note no need to add here required: False for salary, since we
        # configured blank=True in Models


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        exclude = ['id']
        extra_kwargs = {
            'movie': {
                'write_only': True
            }
        }


class CastForMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieActor
        fields = ['actor', 'salary', 'main_role']


class CreateMovieSerializer(serializers.ModelSerializer):


    class Meta:
        model = Movie
        fields = ['id', 'name', 'description', 'duration_in_min', 'release_year', 'cast']
        extra_kwargs = {
            'id': {'read_only': True}
        }
        validators = [
            UniqueTogetherValidator(
                queryset=Movie.objects.all(),
                fields=['name']
            )
        ]

    def create(self, validated_data):
        with transaction.atomic():
            cast_data = validated_data.pop('cast')
            movie = Movie.objects.create(**validated_data)
            for cast in cast_data:
                MovieActor.objects.create(**cast, movie_id=movie.id)
            return movie

    def validate(self, attrs):
        if attrs['release_year'] <= 1920 and attrs['duration_in_min'] >= 60:
            raise ValidationError('Old movies supposed to me short')
        return attrs

