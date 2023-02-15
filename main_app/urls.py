from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('items', views.ItemsList.as_view(), name='index'),
    path('items/myitems/', views.MyItemsList.as_view(), name='items_myitems'),
    path('items/create/', views.ItemCreate.as_view(), name='item_create'),
    path('items/<int:pk>/update/', views.ItemUpdate.as_view(), name='item_update'),
    path('items/<int:pk>/delete/', views.ItemDelete.as_view(), name='item_delete'),
    path('items/<int:pk>/',views.ItemDetail.as_view(), name="item_detail"),
    path('items/<int:item_id>/add_photo/', views.add_photo, name='add_photo'),
    path('trades/', views.TradeList.as_view(), name='trades_index' ),
    path('trades/<int:pk>', views.TradeDetail.as_view(), name='trade_detail'),
    path('trades/create/<int:item_id>',views.TradeCreate.as_view(), name ='trade_create'),
    path('trades/<int:trade_id>/approve/', views.trade_approve, name = 'trade_approve'),
    path('trades/<int:trade_id>/reject/', views.trade_reject, name = 'trade_reject'),
    path('trades/<int:pk>/delete/', views.TradeDelete.as_view(), name='trade_delete'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/login/', views.Login.as_view()),

]

