from django.contrib import admin
from .models import InventoryItem, Category, InventoryChangeLog

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'quantity', 'price', 'category', 'date_added', 'last_updated')
    search_fields = ('name', 'description')
    list_filter = ('category', 'owner')

@admin.register(InventoryChangeLog)
class InventoryChangeLogAdmin(admin.ModelAdmin):
    list_display = ('item', 'changed_by', 'old_quantity', 'new_quantity', 'timestamp', 'reason')
    list_filter = ('changed_by',)
