import uuid
import boto3
import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Item, Trade, Photo
from .forms import UserSignUpForm, UserLoginForm, TradeForm


def index(request):
    return render(request, 'home.html')

class ItemsList(ListView):
  model = Item

  def get_context_data(self, **kwargs):
    context = super(ItemsList, self).get_context_data(**kwargs)
    items = []
    if self.request.user.is_authenticated :
      items = Item.objects.exclude(user = self.request.user)
    else :
      items = Item.objects.all() 
    context['item_list'] = items
    return context

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

class ItemDetail(DetailView):
  model= Item

  def dispatch(self, request, *args, **kwargs):
    self.primary_trades = Trade.objects.filter(item_primary=kwargs['pk'])
    return super().dispatch(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    context = super(ItemDetail, self).get_context_data(**kwargs)
    context['primarytrades'] = self.primary_trades
    return context  

class TradeDetail(LoginRequiredMixin, DetailView):
  model = Trade

class TradeCreate(LoginRequiredMixin, CreateView):
  model = Trade
  form_class = TradeForm

  def get_form_kwargs(self):
    kwargs = super(TradeCreate, self).get_form_kwargs()
    kwargs['user'] = self.request.user
    return kwargs

  def dispatch(self, request, *args, **kwargs):
    self.item_primary = get_object_or_404(Item, pk=kwargs['item_id'])
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    form.instance.item_primary = self.item_primary
    return super().form_valid(form)

class TradeList(LoginRequiredMixin, ListView):
  model = Trade
  def get_context_data(self, **kwargs):
    context = super(TradeList, self).get_context_data(**kwargs)
    trades = []
    for trade in Trade.objects.all():
      if trade.item_primary.user == self.request.user or trade.item_proposed.user == self.request.user:
        trades.append(trade)
    context['trade_list'] = trades
    return context


class TradeDelete(LoginRequiredMixin, DeleteView):
  model = Trade
  success_url = '/trades'

@login_required
def trade_approve(request, trade_id):
  trade = Trade.objects.get(id=trade_id)
  trade.status = '2'
  trade.save()
  return redirect('trades_index')

@login_required
def trade_reject(request, trade_id):
  trade = Trade.objects.get(id=trade_id)
  trade.status = '3'
  trade.save()
  return redirect('trades_index')

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

def add_photo(request, item_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, item_id=item_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('item_detail', pk=item_id)