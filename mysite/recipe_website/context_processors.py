from .models import Categories, Recipes, Summary


def categories(request):
    list_categories = Categories.objects.all()
    recipes = Recipes.objects.all()

    summary = Summary.objects.all()
    dict_categories = {(category.categories_name, category.id): [] for category in list_categories}
    for category in list_categories:
        recipes_id = summary.filter(categories=category.id).values_list('recipes_id', flat=True)
        dict_categories[(category.categories_name, category.id)] = recipes.filter(id__in=recipes_id)
    return {'dict_categories': dict_categories}
