from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from authentication.service import AuthenticationService
from authentication.serializers import SignUpSerializer, UserSerializer


class AuthenticationViewSet(viewsets.ViewSet):
    @action(
        detail=False,
        methods=["post"],
        url_path="signup",
    )
    def sign_up(self, request):
        serializer = SignUpSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        try:
            result =  AuthenticationService.sign_up(serializer.validated_data)
            user_serializer = UserSerializer(result)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Failed to sign up user: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
