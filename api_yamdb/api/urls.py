from django.urls import include, path
from rest_framework import routers

from .views import (
    CategoryViewSet, GenreViewSet,
    TitleViewSet, UserCreateViewSet, UserViewSet
)

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')

auth_urls = [
    path(
        'signup/',
        UserCreateViewSet.as_view({'post': 'create'}),
        name='signup'
    )
]


urlpatterns = [
    path('v1/', include('api.v1.urls')),
    path('auth/', include(auth_urls)),
    path('', include(router.urls))
]
