from uuid import uuid4

from django.core.mail import send_mail

from rest_framework import filters, permissions, status, views, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User

from .permissions import IsAdmin
from .serializers import (AuthUserSignUpSerializer, AuthUserTokenSerializer,
                          UserMeSerializer, UserSerializer)
from .viewsets import  CreateModelViewSet


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin,)
    pagination_class = LimitOffsetPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"


class UserMeView(views.APIView):
    def get(self, request):
        user = self.request.user
        serializer = UserMeSerializer(user, many=False)
        return Response(serializer.data)

    def patch(self, request, pk=None):
        user = self.request.user
        serializer = UserMeSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthSignUpViewSet(CreateModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = AuthUserSignUpSerializer

    @staticmethod
    def generate_confirmation_code():
        return uuid4().hex

    @staticmethod
    def send_confirmation_code(email_to: str, confirmation_code: str):
        email_from = "api_em@em.com"
        subject = "Код подтверждения"

        send_mail(
            subject,
            confirmation_code,
            email_from,
            [email_to],
            fail_silently=False,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        confirmation_code = self.generate_confirmation_code()

        user_filter_params = {
            "username": serializer.initial_data.get("username"),
            "email": serializer.initial_data.get("email"),
        }

        if User.objects.filter(**user_filter_params).exists():
            user = User.objects.get(**user_filter_params)
            user.confirmation_code = confirmation_code
            user.save()
        else:
            serializer.is_valid(raise_exception=True)
            serializer.save(confirmation_code=confirmation_code)

        self.send_confirmation_code(
            serializer.initial_data["email"], confirmation_code
        )

        headers = self.get_success_headers(serializer.initial_data)

        return Response(
            serializer.initial_data, status=status.HTTP_200_OK, headers=headers
        )


class AuthTokenViewSet(TokenObtainPairView):
    serializer_class = AuthUserTokenSerializer
