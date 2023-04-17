from rest_framework import viewsets, status
from rest_framework.viewsets import ViewSet
from .models import Customer, Subscription
from .serializers import CustomerSerializer, SubscriptionSerializer, SubscriptionPriceSerializer, CustomerDataSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from .repositories.subscription_repo import SubscriptionRepo
import datetime

class AccumulatedSubscriptionPriceViewSet(ViewSet):

    @action(detail=True, methods=['get'])
    def accumulated_price(self, request, customer_id=None):
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        if year:
            year = int(year)
        else:
            year = datetime.datetime.now().year

        try:
            if not month:
                raise ParameterMissing('month query parameter is missing')
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        repository = SubscriptionRepo()

        try:
            data = repository.get_accumulated_price_by_month_for(customer_id, int(month), int(year))
            serializer = SubscriptionPriceSerializer(data)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def accumulated_prices_list(self,request):

        month = request.query_params.get('month')
        year = request.query_params.get('year')
        if year:
            year = int(year)
        else:
            year = datetime.datetime.now().year

        try:
            if not month:
                raise ParameterMissing('month query parameter is missing')
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        repository = SubscriptionRepo()

        try:
            data = repository.get_all_accumulated_subscription_prices_for(int(month), int(year))
            serializer = CustomerDataSerializer(data, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

class ParameterMissing(Exception):
    pass