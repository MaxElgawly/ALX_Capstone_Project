from rest_framework import serializers
from .models import InventoryItem, InventoryChangeLog, Category
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name','description')

class InventoryItemSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True, allow_null=True, required=False)

    class Meta:
        model = InventoryItem
        fields = ('id','owner','name','description','quantity','price','category','category_id','date_added','last_updated')

    def validate(self, data):
        if self.instance is None:
            # create
            if 'name' not in data and 'name' not in self.initial_data:
                raise serializers.ValidationError({'name': 'Name is required.'})
            if 'price' not in data and 'price' not in self.initial_data:
                raise serializers.ValidationError({'price': 'Price is required.'})
        return data

class InventoryChangeLogSerializer(serializers.ModelSerializer):
    changed_by = UserSerializer(read_only=True)
    class Meta:
        model = InventoryChangeLog
        fields = ('id','item','changed_by','timestamp','old_quantity','new_quantity','reason')
        read_only_fields = ('timestamp','changed_by','old_quantity')
