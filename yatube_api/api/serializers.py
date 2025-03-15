from django.contrib.auth import get_user_model
from rest_framework import serializers, validators
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Follow, Group, Post


# Serializer for Posts
class PostSerializer(serializers.ModelSerializer):
    """Serializer for posts, including the author's username."""
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


# Serializer for comments
class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments, including the author's username."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post',)


# Serializer for groups
class GroupSerializer(serializers.ModelSerializer):
    """Serializer for groups with read-only fields."""
    
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')
        read_only_fields = ('id', 'title', 'slug', 'description')


# Serializer for Follows
class FollowSerializer(serializers.ModelSerializer):
    """Serializer for follow relationships between users."""
    
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=get_user_model().objects.all(),
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=get_user_model().objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Подписка уже существует'
            ),
        ]

    def validate(self, data):
        """Prevents users from following themselves."""
        if data['user'] == data['following']:
            raise serializers.ValidationError(
                'Попытка подписаться на себя же'
            )
        return data
