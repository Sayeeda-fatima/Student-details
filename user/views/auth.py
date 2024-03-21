from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from user.models import User
from user.serializer import UserModelSerializer
from rest_framework import status
import traceback
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.models import AccessToken, Application
from django.contrib.auth import authenticate
from oauth2_provider.views.base import TokenView



class UserSignupView(APIView):
    def post(self, request, *agrs, **kwargs):
        try:
            data = request.data
            ser = UserModelSerializer(data=data)
            if ser.is_valid():
                ser.save()
                return Response(
                    {"status": "success", "data": {"user": ser.data}},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(ser.errors, status=413)
        except Exception as e:
            traceback.print_exc()
            return Response(str(e), status=500)

class TokenView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            if 'refresh_token' in request.data:
                # Refresh Token Flow
                refresh_token = request.data.get('refresh_token')

                # Retrieve the access token associated with the refresh token
                access_token = AccessToken.objects.get(refresh_token=refresh_token)

                # Verify if the access token is expired
                if access_token.is_refresh_token_expired():
                    return JsonResponse({'error': 'Refresh token has expired'}, status=status.HTTP_400_BAD_REQUEST)

                # Exchange the refresh token for a new access token
                access_token.refresh_token()
                
                return JsonResponse({'access_token': access_token.token})
            else:
                # Access Token Creation Flow
                username = request.data.get("username", None)
                password = request.data.get("password", None)
                
                # Authenticate user
                user = authenticate(username=username, password=password)
                
                if user is not None:
                    # Create or get the OAuth2 application associated with your client
                    application, created = Application.objects.get_or_create(
                        name='Your OAuth2 Client Name',  # Provide your client name here
                        # Add other application details as required
                    )

                    # Create access token
                    access_token = AccessToken.objects.create(
                        user=user,
                        application=application,
                        token_type=AccessToken.BEARER_TOKEN_TYPE,  # Use bearer token type
                    )

                    # Return success response with access token
                    return JsonResponse({'access_token': access_token.token})
                else:
                    # Return error response for invalid credentials
                    return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Return error response for unexpected errors
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UserModelListView(APIView):
    def get(self, request):
        queryset = User.objects.all()
        serializer = UserModelSerializer(queryset, many=True)
        return Response(serializer.data)

