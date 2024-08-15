# authuser/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.contrib.auth import get_user_model, login, authenticate
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from .serializers import UserSerializer, UserUpdateSerializer

import logging

logger = logging.getLogger(__name__)

User = get_user_model()


@method_decorator(ensure_csrf_cookie, name="dispatch")
class GetCSRFToken(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"success": "CSRF cookie set"})


@method_decorator(csrf_protect, name="dispatch")
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@method_decorator(csrf_protect, name="dispatch")
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        print({request.META.get("HTTP_X_CSRFTOKEN")})
        logger.debug(f"Received CSRF token: {request.META.get('HTTP_X_CSRFTOKEN')}")
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return Response(
                {"detail": "Successfully logged in."}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED
            )


@method_decorator(csrf_protect, name="dispatch")
class UpdateUserView(APIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@method_decorator(csrf_protect, name="dispatch")
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(
            {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
        )


class CheckAuthView(APIView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response(
                {
                    "id": request.user.id,
                    "email": request.user.email,
                    "first_name": request.user.first_name,
                    "last_name": request.user.last_name,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED
            )
