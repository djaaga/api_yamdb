from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (AuthSignUpViewSet, AuthTokenViewSet,
                    UserMeView, UserViewSet)

router = SimpleRouter()
router.register('users', UserViewSet)

router.register("auth/signup", AuthSignUpViewSet)

urlpatterns = [
    path("auth/token/", AuthTokenViewSet.as_view()),
    path("users/me/", UserMeView.as_view()),
    path("", include(router.urls)),
]