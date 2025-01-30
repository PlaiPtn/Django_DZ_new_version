from .models import Categories, Recipes, Summary


def categories(request):
    categories = Categories.objects.all()
    recepts = Recipes.objects.all()

    summary = Summary.objects.all()
    list_categories = {(category.categories_name, category.id): [] for category in categories}
    for category in categories:
        recipes_id = summary.filter(categories=category.id).values_list('recipes_id', flat=True)
        list_categories[(category.categories_name, category.id)] = recepts.filter(id__in=recipes_id)
    return {'list_categories': list_categories}
