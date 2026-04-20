from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import GetDebtSerializer
from .services.service import DebtAPIService



class DebtViewSet(viewsets.ViewSet):
    @action(
        detail=False,
        methods=["post"],
        url_path="fetch-singular-debt",
    )
    def get_single_debt(self, request):
        serializer = GetDebtSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = DebtAPIService.fetch_debt(serializer.validated_data)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Failed to fetch debt data: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
