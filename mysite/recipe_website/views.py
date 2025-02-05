
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy
from django.http import HttpRequest
from django.shortcuts import render, redirect
from .models import Recipes, Summary, Categories
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .forms import CustomForm, RecipesForm, MyAuthenticationForm


class MainPageView(ListView):
    model = Recipes
    template_name = 'recipe_website/index.html'
    paginate_by = 5



class MyRecipesView(ListView):
    template_name = 'recipe_website/my_recipes.html'
    paginate_by = 5

    def get_queryset(self):
        return Recipes.objects.filter(user=self.request.user).order_by('-id')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # list_my_recipes = self.get_queryset()
    #     # context['recipes'] = list_my_recipes
    #     return context




class RegisterView(CreateView):
    template_name = 'recipe_website/registration.html'
    form_class = CustomForm
    success_url = '/'
    def form_valid(self, form):
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
    form_class = MyAuthenticationForm



def logout_view(request: HttpRequest):
    logout(request)
    return redirect(reverse('recipe_website:index_page'))


class ReceptCreateView(LoginRequiredMixin, CreateView):
    model = Recipes
    form_class = RecipesForm
    success_url = reverse_lazy('recipe_website:index_page')

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


class ReceptDetailView(DetailView):
    model = Recipes
    template_name = 'recipe_website/recipe_detail.html'
    context_object_name = 'recipe'


class ReceptUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipes
    form_class = RecipesForm
    def get_success_url(self):
        return reverse('recipe_website:my_recept')

class ReceptDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipes
    template_name_suffix = '_delete'
    success_url = reverse_lazy('recipe_website:my_recept')


class CategoriesRecipesListView(ListView):
    template_name = 'recipe_website/category.html'
    paginate_by = 5
    def get_queryset(self):
        summary = Summary.objects.all()
        recipes = Recipes.objects.all()
        categories = Categories.objects.all()
        categories_request = self.request.build_absolute_uri().split('/')[-2]
        list_id_recept = summary.filter(categories=categories_request).values_list('recipes_id', flat=True)
        list_recept = recipes.filter(id__in=list_id_recept).order_by('-id')
        category_name = categories.filter(id=categories_request).values_list('categories_name', flat=True)
        return list_recept, category_name
    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        list_recept, category_name = self.get_queryset()
        contex['recipes'] = list_recept
        contex['category_name'] = ''.join(category_name)
        return contex