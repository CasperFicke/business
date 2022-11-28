# ecommerce/admin.py

# django
from django.contrib import admin

# local
from . import models

# register models
@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status')

@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'item')

@admin.register(models.Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('id','user')

@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id','user' )

@admin.register(models.Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('id',)

@admin.register(models.Line)
class LineAdmin(admin.ModelAdmin):
    list_display = ('id','created')

@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id',)