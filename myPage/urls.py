from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # URL principale del sito
    path('registration/', views.registration, name='registration'),  # URL per la registrazione
    path('login/', views.login, name='login'),  # URL per il login
    path('homepage_client/', views.homepage_client, name='homepage_client'),  # URL per il login
    path('controlla-dati/', views.controlla_dati, name='controlla_dati'),
    path('controlla-username/', views.controlla_username, name='controlla_username'),
    path('inserisci/', views.inserisci_dati, name='inserisci_dati'),
    path('forgot_psw/', views.forgot_psw, name='forgot_psw'),
    path('update_psw_page/', views.update_psw_page, name='update_psw_page'),
    path('update_psw/', views.update_psw, name='update_psw'),
    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),
    path('get_store_data/', views.get_store_data, name='get_store_data'),
    path('get_store_data_for_single_cat/', views.get_store_data_for_single_cat, name='get_store_data_for_single_cat'),
    path('get_store_data_for_single_subcat_or_prov/', views.get_store_data_for_single_subcat_or_prov, name='get_store_data_for_single_subcat_or_prov'),
    path('insert_into_cart/<int:store_id>/', views.insert_into_cart, name='insert_into_cart'),
    path('cart', views.cart, name='cart'),
    path('get_cart_data', views.get_cart_data, name='get_cart_data'),
    path('delete_one_prod_form_cart/<int:cart_id>', views.delete_one_prod_form_cart, name='delete_one_prod_form_cart'),
    path('delete_one_prod_form_cart/<int:cart_id>', views.delete_one_prod_form_cart, name='delete_one_prod_form_cart'),
    path('do_order', views.do_order, name='do_order'),
    path('orders', views.orders, name='orders'),
    path('get_orders_data', views.get_orders_data, name='get_orders_data'),
    path('order_details/<int:order_id>', views.order_details, name='order_details'),
    path('get_order_details_data', views.get_order_details_data, name='get_order_details_data'),
    path('cancel_order', views.cancel_order, name='cancel_order'),
    path('modify_data_account', views.modify_data_account, name='modify_data_account'),
    path('control_psw', views.control_psw, name='control_psw'),
    path('get_data_account', views.get_data_account, name='get_data_account'),
    path('update_datas_account', views.update_datas_account, name='update_datas_account'),
    path('delete_acc_page', views.delete_acc_page, name='delete_acc_page'),
    path('delete_account', views.delete_account, name='delete_account'),
    path('search_product', views.search_product, name='search_product'),
    path('filter_orders_by_status', views.filter_orders_by_status, name='filter_orders_by_status'),
    path('homepage_provider/', views.homepage_provider, name='homepage_provider'),
    path('get_store_data_for_prov/', views.get_store_data_for_prov, name='get_store_data_for_prov'),
    path('get_store_data_for_single_cat_for_prov/', views.get_store_data_for_single_cat_for_prov, name='get_store_data_for_single_cat_for_prov'),
    path('get_store_data_for_single_subcat_for_prov/', views.get_store_data_for_single_subcat_for_prov, name='get_store_data_for_single_subcat_for_prov'),
    path('search_product_for_prov/', views.search_product_for_prov, name='search_product_for_prov'),
]
