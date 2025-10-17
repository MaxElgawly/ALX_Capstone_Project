from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import InventoryItem, InventoryChangeLog, Category
from .serializers import InventoryItemSerializer, InventoryChangeLogSerializer, CategorySerializer
from .permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import transaction
from .models import InventoryItem, InventoryChangeLog, Category
from .serializers import InventoryItemSerializer, InventoryChangeLogSerializer, CategorySerializer
from .permissions import IsOwnerOrReadOnly


class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.select_related('owner','category').all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'category__id': ['exact'],
        'price': ['gte', 'lte'],
        'quantity': ['gte', 'lte'],
    }
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'quantity', 'price','date_added']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        # track quantity changes
        with transaction.atomic():
            instance = self.get_object()
            old_quantity = instance.quantity
            updated = serializer.save()
            new_quantity = updated.quantity
            if old_quantity != new_quantity:
                InventoryChangeLog.objects.create(item=updated, changed_by=self.request.user,
                                                  old_quantity=old_quantity, new_quantity=new_quantity,
                                                  reason=self.request.data.get('reason','Quantity update'))

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def history(self, request, pk=None):
        item = get_object_or_404(InventoryItem, pk=pk)
        logs = item.change_logs.order_by('-timestamp')
        page = self.paginate_queryset(logs)
        serializer = InventoryChangeLogSerializer(page or logs, many=True)
        return self.get_paginated_response(serializer.data) if page is not None else Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# Basic UI views (templates) - simple function views


def item_list_view(request):
    items = InventoryItem.objects.select_related('category','owner').all()
    q = request.GET.get('q')
    if q:
        items = items.filter(name__icontains=q)
    category = request.GET.get('category')
    if category:
        items = items.filter(category__id=category)
    low_stock = request.GET.get('low_stock')
    if low_stock:
        threshold = int(request.GET.get('threshold', 5))
        items = items.filter(quantity__lt=threshold)
    context = {'items': items, 'user': request.user}
    return render(request, 'inventory/item_list.html', context)

def item_detail_view(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    logs = item.change_logs.order_by('-timestamp')[:20]
    context = {'item': item, 'logs': logs}
    return render(request, 'inventory/item_detail.html', context)

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inventory:item_list_ui')
    else:
        form = UserCreationForm()
    return render(request, 'inventory/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('inventory:item_list_ui')
    else:
        form = AuthenticationForm()
    return render(request, 'inventory/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('inventory:item_list_ui')