from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.urls import path
from .views import (RegisterView,
                    logout_view,
                    ReceptCreateView,
                    MainPageView,
                    MyRecipesView,
                    ReceptDetailView,
                    ReceptUpdateView,
                    ReceptDeleteView,
                    CategoriesRecipesListView,
                    Login)

app_name = 'recipe_website'
urlpatterns = [
    path('', MainPageView.as_view(), name='index_page'),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('login/', Login.as_view(template_name='recipe_website/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('create/', ReceptCreateView.as_view(), name='create_recept'),
    path('my-recept/', MyRecipesView.as_view(), name='my_recept'),
    # path('my-recept/', post, name='my_recept'),
    path('recept/<int:pk>/', ReceptDetailView.as_view(), name='recept_detail'),
    path('recept/<int:pk>/update/', ReceptUpdateView.as_view(), name='recept_update'),
    path('recept/<int:pk>/delete/', ReceptDeleteView.as_view(), name='recept_delete'),
    path('category/<int:pk>/<int:user>/', CategoriesRecipesListView.as_view(), name='categories_user'),
    path('category/<int:pk>/', CategoriesRecipesListView.as_view(), name='categories'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)