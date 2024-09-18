# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from .models import Like, Article
# from .serializers import LikeSerializer, ArticleSerializer

import sys, os # 추후 accounts 추가 되고 마이그레이션 한 후 가동해봤을 때 서버 중단 작동하지 않으면 os.quit 로 교체하도록
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Article, Comment, Like, Subscription
from .serializers import ArticleSerializer, CommentSerializer, LikeSerializer, SubscriptionSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# 기사 목록 CR
class ArticleListView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):

        # isFake가 Real 인 경우 바로 서버 종료
        if serializer.validated_data.get('isFake') == 'REAL':
            print("\033[91m\033[1m" + """
+-------------------------------------------------------+
|     !!! 진짜 뉴스 발견 !!!                            |
|     !!! 서버 셧다운 !!!                               |
|     FAKE NEWS 에서는 오직 가짜 뉴스만을 허용합니다.   |
+-------------------------------------------------------+
\033[0m""")
            os._exit(1)  # 서버 강종

        else:

            # isFake가 Fake인 경우 정상적으로 저장
            serializer.save(user=self.request.user)

# 특정 기사 RUD
class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# 특정 기사에 댓글 CR
class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        article = Article.objects.get(pk=self.kwargs['article_pk'])
        serializer.save(user=self.request.user, article=article)

# 댓글 RUD
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    
class LikeCreateView(generics.CreateAPIView):
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        content_type = serializer.validated_data['content_type']
        content_id = serializer.validated_data['content_id']
        user = self.request.user

        # Check if content exists
        if content_type == Like.ARTICLE:
            content = Article.objects.filter(id=content_id).exists()
        elif content_type == Like.COMMENT:
            content = Comment.objects.filter(id=content_id).exists()
        else:
            content = False
        
        if not content:
            raise serializers.ValidationError("Content does not exist.")

        # Save like
        serializer.save(user=user)

class DislikeView(generics.DestroyAPIView):
    queryset = Like.objects.all()

    def delete(self, request, *args, **kwargs):
        content_type = self.kwargs['content_type']
        content_id = self.kwargs['content_id']
        user = request.user

        try:
            like = Like.objects.get(content_type=content_type, content_id=content_id, user=user)
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
class SubscriptionCreateView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        article = Article.objects.get(pk=self.kwargs['article_pk'])
        subscribed_to = article.user

        # 이미 구독 중인지 확인
        if Subscription.objects.filter(subscriber=request.user, subscribed_to=subscribed_to).exists():
            return Response({"detail": "You are already subscribed to this user."}, status=status.HTTP_400_BAD_REQUEST)

        # 구독 생성
        Subscription.objects.create(subscriber=request.user, subscribed_to=subscribed_to)
        return Response({"detail": "Subscription successful!"}, status=status.HTTP_201_CREATED)
    
# 좋아요 목록 조회
class LikeListView(generics.ListAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        content_type = self.kwargs.get('content_type')
        content_id = self.kwargs.get('content_id')

        if content_type == 'article':
            queryset = Like.objects.filter(content_type=Like.ARTICLE, content_id=content_id)
        elif content_type == 'comment':
            queryset = Like.objects.filter(content_type=Like.COMMENT, content_id=content_id)
        else:
            queryset = Like.objects.none()
        
        return queryset
    
# 구독자 목록 조회
class SubscriptionListView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(subscriber=self.request.user)



# # 좋아요 기능 구현
# class LikeArticleView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, article_id):
#         article = Article.objects.get(id=article_id)
#         like, created = Like.objects.get_or_create(user=request.user, article=article)

#         if created:
#             return Response({"message": "좋아요"}, status=status.HTTP_201_CREATED)
#         else:
#             like.delete()
#             return Response({"message": "좋아요 취소"}, status=status.HTTP_200_OK)

# # 기사별 좋아요한 사람들 목록 확인
# class ArticleLikersView(APIView):
#     def get(self, request, article_id):
#         likes = Like.objects.filter(article_id=article_id)
#         likers = [like.user.username for like in likes]
#         return Response(likers, status=status.HTTP_200_OK)

# # 사용자가 좋아요한 기사 목록 확인
# class UserLikedArticlesView(APIView):
#     def get(self, request, user_id):
#         likes = Like.objects.filter(user_id=user_id)
#         liked_articles = [like.article.title for like in likes]
#         return Response(liked_articles, status=status.HTTP_200_OK)