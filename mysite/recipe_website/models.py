from django.contrib.auth.models import User
from django.db import models
from textwrap import shorten


# Create your models here.

class Categories(models.Model):
    categories_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.categories_name


class Recipes(models.Model):
    name_recept = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    ingredients = models.TextField(help_text='После каждого ингредиента ставьте ";" для разделения')
    cooking_steps = models.TextField(help_text='После каждого шага ставьте ";" для разделения')
    cooking_time = models.TimeField(help_text='Формат "чч:мм"')
    image = models.ImageField(upload_to='recipe_website')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_description(self):
        return shorten(self.description, width=150)

    def get_ingredients_list(self):
        return self.ingredients.split(';')

    def get_cooking_steps_list(self):
        return self.cooking_steps.split(';')

    def get_time_str(self):
        return self.cooking_time.strftime('%H:%M').replace(':', 'ч') + 'м'


class Summary(models.Model):
    categories = models.ForeignKey(Categories, on_delete=models.DO_NOTHING, related_name='categories')
    recipes = models.ForeignKey(Recipes, on_delete=models.CASCADE, related_name='recipes')
