import requests
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .services import DebtAPIService


class DebtViewSet(viewsets.ViewSet):
    @action(
        detail=False,
        methods=["get"],
        url_path="fetch-singular-debt",
    )
    def get_single_debt(self, request):
        try:
            result = DebtAPIService.fetch_debt(request.query_params)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': 'Failed to fetch debt data.'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
