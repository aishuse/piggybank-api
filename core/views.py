from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from core.models import Currency, Category, Transaction
from core.serializers import CurrencySerializer, CategorySerializer, ReadTransactionSerializer, \
    WriteTransactionSerializer


class CurrencyListAPIView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class CategoryModelViewset(viewsets.ModelViewSet):
    # queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class TransactionModelViewset(viewsets.ModelViewSet):
    # queryset = Transaction.objects.all()
    # serializer_class = TransactionSerializer

    permission_classes = [IsAuthenticated]

    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['description', ]
    ordering_fields = ['amount', 'date']
    filterset_fields = ['currency__code']

    def get_queryset(self):
        return Transaction.objects.select_related("currency", "category", "user").filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadTransactionSerializer
        return WriteTransactionSerializer

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    # instead of this in serializers.py write,     user = serializers.HiddenField(default=serializers.CurrentUserDefault())


