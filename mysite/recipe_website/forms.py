from django.contrib.auth.forms import UserCreationForm, forms, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


from recipe_website.models import Recipes, Categories, Summary


class CustomForm(UserCreationForm):

    password1 = forms.CharField(
        widget=forms.PasswordInput,
        help_text='',
        validators=[],
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        help_text='Повторите пароль',
        validators=[],
    )

    email = forms.EmailField(
        error_messages={"invalid": "Неверный формат почты"},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Пароль'
        self.fields['email'].label = 'Почта'

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']
        error_messages = {
            'username': {
                'unique': "Пользователь с таким именем уже существует.",
            },
        }
        help_texts = {
            'username': 'Не более 150 символов',

        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с такой почтой уже существует.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                "Пароли не совпадают",
            )
        return cleaned_data

class MyAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя'
        self.fields['password'].label = 'Пароль'
    error_messages = {
    "invalid_login": "Неверные данные",
}




class RecipesForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Categories.objects.all(), help_text='Выберите категорию для рецепта')
    cooking_time = forms.TimeField(help_text='Формат "чч:мм"',
                                   error_messages={'invalid': 'Пожалуйста, введите корректное время в формате ЧЧ:ММ.'})
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name_recept'].label = 'Название рецепта'
        self.fields['description'].label = 'Короткое описание'
        self.fields['ingredients'].label = 'Ингридиенты'
        self.fields['cooking_steps'].label = 'Шаги приготовления'
        self.fields['cooking_time'].label = 'Время приготовления'
        self.fields['image'].label = 'Изображение готового блюда'
        self.fields['category'].label = 'Категория блюда'

    class Meta:
        model = Recipes
        fields = ['name_recept', 'description', 'ingredients', 'cooking_steps', 'cooking_time', 'image']


    def save(self, commit=True):
        recipe = super().save(commit=commit)
        if commit:
            summary, created = Summary.objects.get_or_create(
                recipes=recipe,
                defaults={'categories': self.cleaned_data.get('category')}
            )
            if not created:
                summary.categories = self.cleaned_data.get('category')
                summary.save()
        return recipe