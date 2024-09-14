import sys
import os  # 추후 accounts 추가 되고 마이그레이션 한 후 가동해봤을 때 서버 중단 작동하지 않으면 os.quit 로 교체하도록
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# 기사 목록 CR
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.


# articles 생성과 조회
class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = None  # 페이지네이션 설정 가능
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['user']  # 필터링 가능한 필드 추가(정확히 일치하는것 검색)
    search_fields = ['title', 'content']    # 단어가 포함된것 검색(like)
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
    permission_classes = [IsAuthenticated]
