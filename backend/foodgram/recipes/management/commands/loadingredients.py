import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from recipes.models import Ingredient

DATA_DIR = os.path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):
    help = 'Loads ingredients from a fixture'

    def add_arguments(self, parser):
        parser.add_argument('ingredients_file', type=str)

    def handle(self, *args, **options):
        try:
            print(options['ingredients_file'])
            ingredients_file = os.path.join(
                settings.BASE_DIR, options['ingredients_file']
            )
            fp = open(ingredients_file, 'r')
        except FileNotFoundError:
            raise CommandError('Ingredients file not specified')
        else:
            ingredients_data = json.load(fp)
            ingredients = (
                Ingredient(**ingredient_data)
                for ingredient_data in ingredients_data
            )
            Ingredient.objects.bulk_create(ingredients)
            fp.close()
