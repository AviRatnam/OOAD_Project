from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('new_stocksymbol/', views.new_stocksymbol, name="new_stocksymbol"),
    path('new_transaction/', views.new_transaction, name="new_transaction"),
    path('live_stocks/',views.live_stocks,name="live_stocks"),
    path('user_profile/',views.user_profile,name="user_profile"),
    path('transaction_history/',views.transaction_history,name="transaction_history"),
    path('admin_dashboard/',views.admin_dashboard,name="admin_dashboard"),
    path('stock_history/', views.stock_history, name="stock_history"),
    #path('live_stock_apple/',views.live_stock_apple,name="live_stock_apple"),

]