from django.urls import path
from .views import ArticleListView, ArticleDetailView, CommentListCreateView, CommentDetailView

urlpatterns = [
    # 기사 관련 경로
    path('', ArticleListView.as_view(), name='article-list-create'),  # 기사 목록 조회 및 생성
    path('<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),  # 특정 기사 RUD

    # 댓글 관련 경로
    path('<int:article_pk>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),  # 댓글 목록 조회 및 작성
    path('<int:article_pk>/comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),  # 특정 댓글 RUD
]
