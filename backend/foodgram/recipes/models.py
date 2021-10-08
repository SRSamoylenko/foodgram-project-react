from django.db import models
from django.utils.translation import gettext_lazy as _

from colorfield.fields import ColorField


class Recipe(models.Model):
    ...
    # author
    # name
    # image
    # text
    # ingredients
    # tag
    # cooking_time


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name=_('Ingredient name'),
        max_length=150,
        unique=True,
    )
    measurement_unit = models.CharField(
        verbose_name=_('Measurement unit'),
        max_length=25,
    )

    class Meta:
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')
        ordering = ('name',)


class Tag(models.Model):
    name = models.CharField(
        verbose_name=_('Tag name'),
        max_length=150,
        unique=True,
    )
    colour = ColorField(
        verbose_name=_('Tag color'),
        unique=True,
    )
    slug = models.SlugField(
        verbose_name=_('Slug'),
        unique=True,
    )

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ('name', 'slug')


class Favorite(models.Model):
    ...
