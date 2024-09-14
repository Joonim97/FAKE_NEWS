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
                  'user', 'comments', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        # 수정할 수 없는 필드
        immutable_fields = ['isFake']

        # 수정할 수 없는 필드에 대한 값 제거
        for field in immutable_fields:
            validated_data.pop(field, None)

        # 기본 update 메서드 호출
        return super().update(instance, validated_data)
