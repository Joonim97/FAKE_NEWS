from rest_framework import serializers
from .models import Article, Comment, Like, Subscription

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
        fields = ['id', 'title', 'description', 'isFake', 'user', 'comments'] 
        read_only_fields = ['user', 'created_at']
        
        
        
        
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'content_type', 'content_id', 'user']
        read_only_fields = ['user']
        
class SubscriptionSerializer(serializers.ModelSerializer):
    subscriber = serializers.CharField(source='subscriber.username', read_only=True)
    subscribed_to = serializers.CharField(source='subscribed_to.username', read_only=True)

    class Meta:
        model = Subscription
        fields = ['subscriber', 'subscribed_to', 'created_at']
        read_only_fields = ['subscriber', 'subscribed_to', 'created_at']


# class LikeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Like
#         fields = ['user', 'article', 'liked_at']

# class ArticleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Article
#         fields = ['id', 'title', 'content']