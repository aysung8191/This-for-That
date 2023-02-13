from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('items', views.ItemsList.as_view(), name='index'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/login/', views.Login.as_view()),
]

