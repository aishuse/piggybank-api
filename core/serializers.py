from django.contrib.auth.models import User
from rest_framework import serializers

from core.models import Currency, Category, Transaction


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'code', 'name']


class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'username', 'email']


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # user = ReadUserSerializer()

    class Meta:
        model = Category
        fields = ['id', 'name', 'user']


class WriteTransactionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    currency = serializers.SlugRelatedField(slug_field="code", queryset=Currency.objects.all())

    class Meta:
        model = Transaction
        fields = ['user', 'amount', 'currency', 'date', 'description', 'category']

# logged in user should do the transactions with category created by him only
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context["request"].user
        self.fields["category"].queryset = Category.objects.filter(user=user) # or using related name
                                        # user.categories.all()





class ReadTransactionSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()
    category = CategorySerializer()
    user = ReadUserSerializer()
    class Meta:
        model = Transaction
        fields = ['user', 'amount', 'currency', 'date', 'description', 'category']
        read_only_fields = fields



