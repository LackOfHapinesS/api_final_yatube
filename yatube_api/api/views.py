from django.shortcuts import get_object_or_404
from rest_framework import (
    filters, mixins, pagination, permissions, viewsets
)

from posts.models import Comment, Follow, Group, Post
from .serializers import (
    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer
)
from .permissions import OwnershipPermission


# Base ViewSet with ownership permission
class PermissionViewset(viewsets.ModelViewSet):
    """Viewset that applies custom ownership permissions."""
    permission_classes = (OwnershipPermission,)


# ReadOnly ViewSet for Groups
class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Provides a read-only API for groups."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(PermissionViewset):
    """Handles CRUD operations for posts."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = pagination.LimitOffsetPagination

    def perform_create(self, serializer):
        """Assigns the author before saving a new post."""
        return serializer.save(author=self.request.user)


class CommentViewSet(PermissionViewset):
    """Handles CRUD operations for comments on posts."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Returns comments for the specified post."""
        return self.get_post().comments.all()

    def get_post(self):
        """Helper method to retrieve the post object."""
        return get_object_or_404(Post, pk=self.kwargs.get('post_pk'))

    def perform_create(self, serializer):
        """Assigns author and related post before saving a comment."""
        return serializer.save(author=self.request.user, post=self.get_post())


class FollowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Handles following and listing followers."""
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """Returns the followers of the current user."""
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        """Assigns the user before creating a follow record."""
        serializer.save(user=self.request.user)
