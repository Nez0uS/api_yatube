from rest_framework import serializers
from posts.models import Post, Group, Comment


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для постов"""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Post
        read_only_fields = ('pub_date',)


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для групп (только чтение)"""
    class Meta:
        fields = '__all__'
        model = Group
        read_only_fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев"""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('created', 'post')
