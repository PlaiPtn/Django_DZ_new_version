
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.http import HttpRequest
from django.shortcuts import redirect
from .models import Recipes, Summary, Categories
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .forms import CustomForm, RecipesForm, MyAuthenticationForm

import logging

log = logging.getLogger(__name__)

class MainPageView(ListView):
    """
        Страница главная
    """

    template_name = 'recipe_website/index.html'
    paginate_by = 5
    def get_queryset(self):
        if self.request.user.is_authenticated:
            log.info("Пользователь %s открыл главную страницу", self.request.user.username )
        else:
            log.info("Анонимный пользователь открыл главную страницу")
        return Recipes.objects.all().order_by('-id')

class MyRecipesView(ListView):
    """
        Страница моих рецептов
    """

    template_name = 'recipe_website/my_recipes.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        log.info("Пользователь %s открыл страницу мои рецепты", self.request.user.username)
        if 'pk' in self.kwargs:
            categories_request = self.kwargs['pk']
            return (Summary.objects.filter(categories=categories_request)
                    .select_related("recipes").prefetch_related('recipes__user').
                    filter(recipes__user__username=self.request.user.username).order_by('-id'))
        return Summary.objects.all().select_related("recipes").prefetch_related('recipes__user').order_by('-id')

class RegisterView(CreateView):
    """
        Страница регистрации
    """

    template_name = 'recipe_website/registration.html'
    form_class = CustomForm
    success_url = '/'
    log.info("Происходит регистрация")
    def form_valid(self, form):
        log.info("Регистрация прошла успешна")
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        email = form.cleaned_data.get('email')
        user = form.save()
        user.email = email
        user.set_password(password)
        user.save()

        user = authenticate(
            self.request,
            username=username,
            password=password
        )
        login(request = self.request, user = user)
        return super().form_valid(form)

class Login(LoginView):
    """
        Страница авторизации
    """

    form_class = MyAuthenticationForm
    log.info("Авторизация")
    def form_valid(self, form):
        login_username = form.cleaned_data.get('username')
        login_password = form.cleaned_data.get('password')

        user = authenticate(username=login_username, password=login_password)


        if user is not None:
            log_message = f"Пользователь {login_username} успешно авторизован"
            log.info(log_message)
            return super().form_valid(form)
        else:
            log.info(f"Неудачная попытка авторизации для {login_username}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        log.info("Неудачная попытка авторизации")
        return super().form_invalid(form)

def logout_view(request: HttpRequest):
    """
        Страница выхода из акк
    """

    log.info('Пользователь %s вышел из аккаунта', str(request.user.username))
    logout(request)
    return redirect(reverse('recipe_website:index_page'))

class ReceptCreateView(LoginRequiredMixin, CreateView):
    """
        Страница создания рецепта
    """

    model = Recipes
    form_class = RecipesForm
    success_url = reverse_lazy('recipe_website:index_page')

    def get(self, request, *args, **kwargs):
        log.info('Пользователь %s зашел на страницу создания рецепта', self.request.user.username)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        log.info('Пользователь %s создал новый рецепт', self.request.user.username)
        form.instance.user = self.request.user
        return super().form_valid(form)

class ReceptDetailView(DetailView):
    """
        Страница просмотра рецепта
    """

    model = Recipes
    template_name = 'recipe_website/recipe_detail.html'
    context_object_name = 'recipe'
    def get(self, request, *args, **kwargs):
        log.info('Пользователь %s смотрит рецепт %s',
                 self.request.user.username, self.model.objects.get(pk=kwargs['pk']).name_recept)
        return super().get(request, *args, **kwargs)

class ReceptUpdateView(LoginRequiredMixin, UpdateView):
    """
        Страница редактирования рецепта
    """

    model = Recipes
    form_class = RecipesForm
    def get(self, request, *args, **kwargs):
        log.info('Пользователь %s редактирует рецепт %s',
                 self.request.user.username, self.model.objects.get(pk=kwargs['pk']).name_recept)
        return super().get(request, *args, **kwargs)
    def get_success_url(self):
        return reverse('recipe_website:my_recept')

class ReceptDeleteView(LoginRequiredMixin, DeleteView):
    """
        Страница удаления рецепта
    """

    model = Recipes
    template_name_suffix = '_delete'
    success_url = reverse_lazy('recipe_website:my_recept')
    def get(self, request, *args, **kwargs):
        log.info('Пользователь %s удаляет рецепт %s',
                 self.request.user.username, self.model.objects.get(pk=kwargs['pk']).name_recept)
        return super().get(request, *args, **kwargs)

class CategoriesRecipesListView(ListView):
    """
        Страница списка рецептов по категории
    """

    template_name = 'recipe_website/category.html'
    paginate_by = 5
    def get_queryset(self, user=None, **kwargs):
        categories_request = self.kwargs['pk']
        list_recept = (Summary.objects.filter(categories=categories_request).select_related("recipes").
            prefetch_related('recipes__user').order_by('-id'))
        return list_recept
    def get_context_data(self, *args, **kwargs):
        categories_request = self.kwargs['pk']
        context = super().get_context_data(*args, **kwargs)
        context['category_name'] = ''.join(Categories.objects.filter(id=categories_request).
                                           values_list('categories_name', flat=True))
        return context
