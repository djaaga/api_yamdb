from django.shortcuts import get_object_or_404

from rest_framework import viewsets

from reviews.models import Review, Title

from .permissions import ReviewPermission

from .serializers import (CommentSerializer,
                          ReviewSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы c отзывами."""
    serializer_class = ReviewSerializer
    permission_classes = (ReviewPermission,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы c комментариями."""
    serializer_class = CommentSerializer
    permission_classes = (ReviewPermission,)

    def get_queryset(self):
        """Позволяет получить комментарии к отдельному отзыву."""
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, id=self.kwargs['review_id'],
            title=self.kwargs['title_id']
        )
        serializer.save(author=self.request.user, review=review)
