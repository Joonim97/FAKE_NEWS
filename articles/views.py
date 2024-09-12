from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Article
from .serializers import ArticleSerializer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.


# articles 생성과 조회
class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = None  # 페이지네이션 설정 가능
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['author']  # 필터링 가능한 필드 추가(정확히 일치하는것 검색)
    search_fields = ['title', 'content']    # 단어가 포함된것 검색(like)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# article 상세페이지 조회
class ArticleDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


# articles 수정과 삭제
class ArticleUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        article = super().get_object()
        if article.author != self.request.user:
            raise PermissionDenied("니꺼 아니야")
        return article
