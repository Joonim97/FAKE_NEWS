from django.urls import path
from .views import LikeArticleView, ArticleLikersView, UserLikedArticlesView

urlpatterns = [
    path('articles/<int:article_id>/like/', LikeArticleView.as_view(), name='like-article'),
    path('articles/<int:article_id>/likers/', ArticleLikersView.as_view(), name='article-likers'),
    path('users/<int:user_id>/liked-articles/', UserLikedArticlesView.as_view(), name='user-liked-articles'),
]
