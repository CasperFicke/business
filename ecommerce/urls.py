# ecommerce/urls.py

# django
from django.urls import path

# local
from . import views

app_name = "ecommerce"

urlpatterns = [
  path('items/'               , views.ItemsView.as_view(), name='items'),        # returns listview of all items in stock
  path('item/<slug:slug>/'    , views.ItemView.as_view(), name='item'),          # returns detailpage of an item
	path('items/add-or-remove/' , views.add_or_remove_item, name='add_or_remove'), # returns a json response
	path('checkout/'            , views.CheckoutView.as_view(), name="checkout"),  # returns 
	path('pay/'                 , views.stripe_payment, name="pay"),               # returns a json response
	path('cart/'                , views.CartView.as_view(), name="cart"),          # returns
	path('orders/'              , views.OrdersView.as_view(), name="orders"),      # returns
	path('order/<int:id>/'      , views.OrderView.as_view(), name="order"),        # returns detailpage of an order
	path('update-source/'       , views.update_source, name="update-source"),      # returns a json response
	]