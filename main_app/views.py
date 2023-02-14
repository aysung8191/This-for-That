from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Item, Trade
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
    try:
      self.primary_trades = Trade.objects.filter(item_primary=kwargs['pk'])
    except:
      self.primary_trades = ''
    return super().dispatch(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    context = super(ItemDetail, self).get_context_data(**kwargs)
    print(self.primary_trades)
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