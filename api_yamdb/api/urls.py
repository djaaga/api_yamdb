from django.urls import include, path

from rest_framework.routers import DefaultRouter

from user.views import ObtainToken, SignUpViewSet, UserViewSet

from api.views import CategoryViewSet, CommentViewSet, ReviewViewSet

app_name = 'api'

v1_router = DefaultRouter()

v1_router.register('auth/signup', SignUpViewSet)
v1_router.register('users', UserViewSet)
v1_router.register('categories', CategoryViewSet)
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet,
                   basename='reviews')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                   CommentViewSet,
                   basename='comments')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/token/', ObtainToken),
]