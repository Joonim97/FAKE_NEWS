from django.urls import path
# from .views import LikeArticleView, ArticleLikersView, UserLikedArticlesView
from .views import ArticleListView, ArticleDetailView, CommentListCreateView, CommentDetailView, LikeCreateView, DislikeView, LikeListView, SubscriptionCreateView

urlpatterns = [
    # 기사 관련 경로
    path('', ArticleListView.as_view(), name='article-list-create'),  # 기사 목록 조회 및 생성
    path('<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),  # 특정 기사 RUD

    # 댓글 관련 경로
    path('<int:article_pk>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),  # 댓글 목록 조회 및 작성
    path('<int:article_pk>/comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),  # 특정 댓글 RUD
    
    path('articles/<int:article_pk>/likes/', LikeCreateView.as_view(), name='article-like-create'),
    path('comments/<int:comment_pk>/likes/', LikeCreateView.as_view(), name='comment-like-create'),
    path('likes/<str:content_type>/<int:content_id>/', DislikeView.as_view(), name='like-delete'),
    path('<int:article_pk>/likes/articles/', LikeListView.as_view(), name='article-like-list'),
    path('<int:comment_pk>/likes/comments/', LikeListView.as_view(), name='comment-like-list'),
    path('articles/<int:article_pk>/subscribe/', SubscriptionCreateView.as_view(), name='subscribe-author'),
    
    
    # path('<int:article_id>/like/', LikeArticleView.as_view(), name='like-article'),
    # path('<int:article_id>/likers/', ArticleLikersView.as_view(), name='article-likers'),
    # path('users/<int:user_id>/liked-articles/', UserLikedArticlesView.as_view(), name='user-liked-articles'),
]
