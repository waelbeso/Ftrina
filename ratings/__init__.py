from __future__ import unicode_literals

from .app_settings import Settings

__version__ = '0.5.5'

default_app_config = 'ratings.apps.RatingsConfig'
app_settings = Settings()


def get_star_ratings_rating_model_name():
    return swapper.get_model_name('ratings', 'Rating')


def get_star_ratings_rating_model():
    return swapper.load_model('ratings', 'Rating')
