import sys, os # 추후 accounts 추가 되고 마이그레이션 한 후 가동해봤을 때 서버 중단 작동하지 않으면 os.quit 로 교체하도록
from rest_framework import generics
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# 기사 목록 CR
class ArticleListView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):

        # isFake가 Real 인 경우 바로 서버 종료
        if serializer.validated_data.get('isFake') == 'REAL':
            serializer.save(user=self.request.user)
            print("찐 뉴스 발견. 서버 강종.")

            sys._exit(1)  # 서버 강종

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
