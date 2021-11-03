from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


from .models import Schema, Column


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    # password = forms.PasswordInput()

class CreateSchemaForm(forms.ModelForm):

    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'class': 'form-input'}))
    DELIMITERS = (
        (',' ','),
        (';' ';'),
        ('*' '*'),

    )
    delimiter = forms.ChoiceField(choices=DELIMITERS)
    class Meta:
        model = Schema
        fields = ('title',)

class CreateColumnForm(forms.ModelForm):

    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'class': 'form-input'}))


    LOAN_STATUS = (
        ('Name', 'Name'),
        ('Company', 'Company'),
        ('E-mail', 'E-mail'),
        ('Address', 'Address'),
        ('Age', 'Age'),
        ('Phone number', 'Phone number'),

    )

    order = forms.IntegerField()
    type = forms.ChoiceField(choices=LOAN_STATUS)

    class Meta:
        model = Column
        fields = ('title', 'order', 'type')


    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['username'].label = "Username"
    #     self.fields['password'].label = "Password"
    #
    # def cleaned_data(self):
    #     username = self.cleaned_data['username']
    #     password = self.cleaned_data['password']
    #     if not User.objects.filter(username=username).exists():
    #         raise forms.ValidationError(f'User with login {username} not found')
    #     user = User.objects.filter(username=username).first()
    #     if user:
    #         if not user.check_password(password):
    #             raise forms.ValidationError('Wrong password! Please enter correct password')
    #     return self.cleaned_data
    #
    # class Meta:
    #     model = User
    #     fields = ['username', 'password']