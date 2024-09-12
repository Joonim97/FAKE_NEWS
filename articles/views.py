from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Like, Article
from .serializers import LikeSerializer, ArticleSerializer

# 좋아요 기능 구현
class LikeArticleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, article_id):
        article = Article.objects.get(id=article_id)
        like, created = Like.objects.get_or_create(user=request.user, article=article)

        if created:
            return Response({"message": "좋아요"}, status=status.HTTP_201_CREATED)
        else:
            like.delete()
            return Response({"message": "좋아요 취소"}, status=status.HTTP_200_OK)

# 기사별 좋아요한 사람들 목록 확인
class ArticleLikersView(APIView):
    def get(self, request, article_id):
        likes = Like.objects.filter(article_id=article_id)
        likers = [like.user.username for like in likes]
        return Response(likers, status=status.HTTP_200_OK)

# 사용자가 좋아요한 기사 목록 확인
class UserLikedArticlesView(APIView):
    def get(self, request, user_id):
        likes = Like.objects.filter(user_id=user_id)
        liked_articles = [like.article.title for like in likes]
        return Response(liked_articles, status=status.HTTP_200_OK)
