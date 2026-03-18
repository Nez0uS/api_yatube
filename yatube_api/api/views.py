from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from posts.models import Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для постов"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """При создании поста проставляем текущего автора"""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Разрешаем редактировать только автору"""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super().perform_update(serializer)

    def perform_destroy(self, serializer):
        """Разрешаем удалять только автору"""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super().perform_destroy(serializer)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для групп (только чтение)"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Возвращаем комментарии только для конкретного поста"""
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        """При создании комментария проставляем автора и пост"""
        post_id = self.kwargs.get('post_id')
        serializer.save(author=self.request.user, post_id=post_id)

    def perform_update(self, serializer):
        """Разрешаем редактировать только автору"""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super().perform_update(serializer)

    def perform_destroy(self, serializer):
        """Разрешаем удалять только автору"""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super().perform_destroy(serializer)
