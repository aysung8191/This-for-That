from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django import forms
from django.contrib.auth.models import User


class UserSignUpForm(UserCreationForm):
   class Meta:
      model = User
      fields = ['username', 'password1', 'password2']
   
   username = UsernameField(widget=forms.TextInput(attrs={'placeholder': 'username'}), label='', help_text = '150 characters or fewer. Letters, digits and @/./+/-/_ only.')
   password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}), label='', help_text = 'Your password can’t be entirely numeric.')
   password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password confirmation'}), label='')


class UserLoginForm(AuthenticationForm):
  def __init__(self, *args, **kwargs):
     super(UserLoginForm, self).__init__(*args, **kwargs)

  username = UsernameField(widget=forms.TextInput(attrs={'placeholder': 'username'}), label='')
  password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}), label='')