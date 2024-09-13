from rest_framework import serializers
from .models import Article, Comment

# 댓글 관련 시리얼라이저
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'article', 'text', 'created_at']
        read_only_fields = ['user', 'article', 'created_at']

# 기사 관련 시리얼라이저 (댓글 포함)
class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'isFake', 'image',
                  'user', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']
