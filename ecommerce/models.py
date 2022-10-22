# ecommerce/models.py

# django
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# installed packages
from djmoney.models.fields import MoneyField
from django_extensions.db.models import (
  TimeStampedModel,
  ActivatorModel,
  TitleSlugDescriptionModel
)

# Items in stock
class Item(
  TimeStampedModel, # add created- and modified timefield to the model
  ActivatorModel , # add isactive boolean to the model
  TitleSlugDescriptionModel, # add title, slug and description to the model
  models.Model):
  """
  ecommerce.Item
  Stores a single item entry for our shop
  """
  class Meta:
    verbose_name        = 'Item'
    verbose_name_plural = 'Items'
    ordering            = ["id"]
  # attributes
  image = models.ImageField(default='default_item_image.jpg', upload_to='items', null=True, blank=True)
  stock = models.IntegerField(default=1)
  # variable price to make the customer pay the price of the item it has at the moment the item is put in the shopping cart
  variable_price     = MoneyField(
    max_digits       = 14, 
    decimal_places   = 2, 
    default_currency ='EUR', 
    null             = True,
    blank            = True)

  # price in cents ( because stripe demands integers)
  def amount(self):
    amount = int(self.variable_price.amount * 100)
    return amount

  def get_absolute_url(self):
    return f'/item/{self.slug}/'
    
# Cartitemmanager; 
class CartItemManager(models.Manager):
  """
  A Manager for Cart item objects
  """
  # 
  def get_query_set(self):
    return self.get_queryset()
  # empty the shopping cart
  def clear_items(self, user):
    '''
    Used to remove all cart items after payment is processed
    Useage - CartItem.objects.clear_items(auth.User)
    '''
    qs = self.get_query_set().filter(
      user = user
    )
    for q in qs:
      q.delete()

# CartItem; an item in a shopping cart
class CartItem(
  TimeStampedModel,
  ActivatorModel ,
  models.Model):
  """
  ecommerce.CartItem
  Stores a single item entry, related to :model:`ecommerce.Item` and
  :model:`auth.User`.
  """
  class Meta:
    verbose_name        = 'Item in cart'
    verbose_name_plural = 'Items in cart'
    ordering            = ["id"]
  # attributes
  quantity = models.IntegerField(default=0)
  # relaties
  user     = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  item     = models.ForeignKey(Item, null=True, blank=True, on_delete=models.CASCADE)

  # number of ....
  def amount(self):
    amount = self.item.amount() * self.quantity
    return amount

  # connect manager to cartitem
  objects = CartItemManager()

# Shopping cart van een user evt gevuld met cart items
class Cart(
  TimeStampedModel,
  ActivatorModel ,
  models.Model):
  """
  ecommerce.Cart
  This is a Users Shopping cart, related to :model:`auth.User`.
  """
  class Meta:
    verbose_name        = 'User cart'
    verbose_name_plural = 'User cart'
    ordering            = ["id"]
  # relaties
  user  = models.OneToOneField(User, on_delete=models.CASCADE)   
  items = models.ManyToManyField(CartItem, blank=True)
  # totaal aantal items in the shopping cart
  def item_count(self):
    count = 0
    for obj in self.items.all():
      count += obj.quantity
    return count
  # totale prijs van alle items in the shopping cart
  def amount(self):
    count = 0
    for obj in self.items.all():
      count += obj.amount()
    return int(count)
  # add or remove items to or from the shopping cart
  def add_or_remove(self, action, object):
    '''
    Used to easily add or remove users to the cart model
    '''
    match action:
      case "add":
        if object not in self.items.all():
          self.items.add(object)
      case "remove":
        self.items.remove(object)
    self.save()
  # check if item is in the shopping cart
  def item_check(self, item):
    '''
    Checks if an item is in the User cart
    '''
    cartitems = [i.item  for i in self.items.all()]
    if item in cartitems:
      return True
    return False
  # check number of items in shopping cart
  def qty_check(self, item):
    try:
      cart_item = CartItem.objects.get(item = item, user = self.user)
      return cart_item.quantity
    except CartItem.DoesNotExist:
      return 0.0

# tbv stripe: Source
class Source(
  TimeStampedModel,
  ActivatorModel ,
  models.Model):
  """
  ecommerce.Source
  Stores Stripe ID's for sources (payment methods).
  """
  class Meta:
    verbose_name        = 'Source'
    verbose_name_plural = 'Sources'
    ordering            = ["id"]
  # attributes
  stripe_id  = models.CharField(max_length=100)
  is_default = models.BooleanField(default=False)

# invoice line; factuurregel. een regel per itemtype
class Line(
  TimeStampedModel,
  ActivatorModel ,
  models.Model):
  '''
  ecommerce.Line
  Stores a single line entry, related to :model:`ecommerce.Item` and
  :model:`auth.User`.
  '''
  class Meta:
    verbose_name        = 'Invoice Line'
    verbose_name_plural = 'Invoice Lines'
    ordering            = ["id"]
  # attributes
  amount    = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR', null=True, blank=True)
  stripe_id = models.CharField(max_length=100)
  quantity  = models.IntegerField(default=1, blank=True,null=True)
  # relaties
  user      = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)   
  item      = models.ForeignKey(Item, on_delete=models.SET_NULL, blank=True, null=True)
  
# Invoice; factuur. totale factuur, alle factuurregels
class Invoice(
  TimeStampedModel,
  ActivatorModel ,
  models.Model):
  '''
  ecommerce.Invoice
  Stores a single invoice entry, related to :model:`ecommerce.Line`,
  :model:`ecommerce.Source` and :model:`auth.User`.
  '''
  class Meta:
    verbose_name        = 'User Invoice'
    verbose_name_plural = 'User Invoices'
    ordering            = ["id"]
  # attributes
  stripe_id = models.CharField(max_length=100)
  # relaties
  user      = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)   
  source    = models.ForeignKey(Source, on_delete=models.SET_NULL, blank=True, null=True) 
  lines     = models.ManyToManyField(Line, blank=True)
  # totaal aantal items van factuur
  def item_count(self):
      count = 0
      for obj in self.lines.all():
          count += obj.quantity
      return count
  # totaal bedrag van factuur
  def amount(self):
      count = 0
      for obj in self.lines.all():
          count += obj.buy_amount * obj.quantity
      return count
  # 
  def wallet(self):
      wallet = Wallet.objects.for_source(self.source)
      return wallet

# Walletmanager
class WalletManager(models.Manager):
  """
  A Manager for Wallet objects
  """
  # 
  def get_query_set(self):
    return self.get_queryset()
  # 
  def for_source(self, source):
    """
    Returns a Wallet objects queryset for a given source model.
    Usage:
      Source = Source.objects.first()
      Wallet.objects.for_source(Source)
    """
    qs = self.get_query_set().filter(
      sources = source
    )
    return qs

# Wallet
class Wallet(TimeStampedModel, ActivatorModel):
  '''
  ecommerce.Wallet
  Stores a single wallet entry related to :model:`ecommerce.Invoice`,
  :model:`ecommerce.Source` and :model:`auth.User`.
  '''
  class Meta:
    verbose_name        = 'User Wallet'
    verbose_name_plural = 'User Wallets'
    ordering            = ["id"]
  # attributes
  stripe_id = models.CharField(max_length=100, blank=True, null=True)
  # relaties
  user      = models.OneToOneField(User, on_delete=models.CASCADE)
  invoices  = models.ManyToManyField(Invoice, blank=True)
  sources   = models.ManyToManyField(Source, blank=True)
  # 
  objects   = WalletManager()