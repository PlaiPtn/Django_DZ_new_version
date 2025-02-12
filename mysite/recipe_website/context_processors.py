from .models import Categories, Recipes, Summary


def categories(request):
    """
        Боковое меню рецептов по категориям
    """

    list_categories = Categories.objects.all()
    recipes = Recipes.objects.all()
    summary = Summary.objects.all()
    dict_categories = {(category.categories_name, category.pk): [] for category in list_categories}
    for category in list_categories:
        recipes_id = summary.filter(categories=category.pk).values_list('recipes_id', flat=True)
        dict_categories[(category.categories_name, category.pk)] = recipes.filter(id__in=recipes_id).order_by('-id')[:4]
    return {'dict_categories': dict_categories}
