from django import forms
from django.contrib.auth.forms import UserCreationForm
from basics.models import MyUser, Business, TypeBusiness, Category, Favorites


class LoginForm(forms.Form):
    username = forms.CharField(label="User Name", max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())

class Search(forms.Form):
    searcher = forms.CharField(max_length=64)

USER_CHOICES= (
 ('business_owner', 'Business Owner'),
 ('user', 'User'),
)

class SignUpForm(UserCreationForm):
    date_of_birth = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    bio = forms.CharField()
    avatar = forms.ImageField()
    type_of_user = forms.ChoiceField(choices=USER_CHOICES)

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'password1', 'password2', 'bio', 'type_of_user', 'avatar')

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ('name', 'description','logo','address', 'telephone', 'type_of_business', 'category','photo')

class FavoritesForm(forms.ModelForm):
    class Meta:
        model = Favorites
        fields = ('person','business')
