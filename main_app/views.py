from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Item, Trade
from .forms import UserSignUpForm, UserLoginForm


def index(request):
    return render(request, 'home.html')

class ItemsList(ListView):
  model = Item

class MyItemsList(LoginRequiredMixin,ListView):
  model = Item
  template_name = 'items/my_items.html'
  def get_context_data(self, **kwargs):
        context = super(MyItemsList, self).get_context_data(**kwargs)
        context['items'] = Item.objects.filter(user = self.request.user)
        return context
  
class ItemCreate(LoginRequiredMixin, CreateView):
  model = Item
  fields = ['name', 'description']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)
  
class ItemUpdate(LoginRequiredMixin, UpdateView):
  model = Item
  fields = ['name', 'description']

class ItemDelete(LoginRequiredMixin, DeleteView):
  model = Item
  success_url = '/items/myitems'

class TradeCreate(LoginRequiredMixin, CreateView):
  model = Trade
  fields = ['item_proposed', 'comment' , 'status']

  def form_valid(self, form):
    form.instance.item_primary = self.request.user
    return super().form_valid(form)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserSignUpForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserSignUpForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class Login(LoginView):
  authentication_form = UserLoginForm