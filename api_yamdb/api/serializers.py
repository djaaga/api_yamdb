from rest_framework import serializers

from reviews.models import Category, Comment, Review


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    comment = CommentSerializer(read_only=True, many=True)
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор Категории."""

    class Meta:
        model = Category
        fields = ('name', 'slug')