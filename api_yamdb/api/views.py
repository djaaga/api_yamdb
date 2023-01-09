from django.shortcuts import get_object_or_404

from rest_framework import mixins, viewsets

from rest_framework.permissions import IsAuthenticated

from reviews.models import Review

from .permissions import IsOwnerOrReadOnly

from .serializers import (CommentSerializer,
                          ReviewSerializer)


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Миксин для получения всех объектов, создания, и удаления."""

    pass


class ReviewViewSet(viewsets.ModelViewSet):
    """Просмотр, добавление, редактирование, удаление отзыва."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)

    def get_queryset(self):
        """Позволяет получить комментарии к отдельному отзыву."""

        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review_id=self.kwargs.get('review_id')
        )
