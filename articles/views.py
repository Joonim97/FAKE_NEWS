import sys, os, ollama # 추후 accounts 추가 되고 마이그레이션 한 후 가동해봤을 때 서버 중단 작동하지 않으면 os.quit 로 교체하도록
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Article, Comment, Like, Subscription_test
from .serializers import ArticleSerializer, CommentSerializer, LikeSerializer, SubscriptionSerializer

# 기사 목록 CR
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


# 가짜뉴스 생성기
class FakeNewsGenerator(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def generator(self, topic):
        prompt = f"{topic} 라는 주제에 맞는 가짜 뉴스의 제목과 기사를 작성해달라. 제목과 기사 사이에는 문단 나눔이 되어있어야한다. 뉴스의 내용은 허황되며, 음모론으로 가득차야한다. 또한 그 거짓정보가 진실인것마냥 확신에 찬 어조를 채택해야한다. 텍스트는 최대 200자로 제한한다."
        response = ollama.chat(
            model='llama3.1',
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response['message']['content']

    def post(self, request, *args, **kwargs):
        topic = request.data.get('topic')

        if not topic:
            return Response({"error": "주제 미입력됨."}, status=400)

        # Ollama로 가짜 뉴스 생성
        title, content = self.generator(topic).split("\n", 1)

        # Article 데이터로 저장, 현재 사용자 할당
        article_data = {
            "title": title.strip(),
            "content": content.strip(),
            "isFake": "FAKE",
        }

        serializer = self.get_serializer(data=article_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=201)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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
    

class LikeView(APIView):
    serializer_class = LikeSerializer
    
    def get(self, request, content_type, content_id):
        if content_type == Like.ARTICLE:
            queryset = Like.objects.filter(content_type=Like.ARTICLE, content_id=content_id)
        elif content_type == Like.COMMENT:
            queryset = Like.objects.filter(content_type=Like.COMMENT, content_id=content_id)
        else:
            queryset = Like.objects.none()

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, content_type, content_id):
        data = request.data.copy()
        data['content_type'] = content_type  # URL에서 받은 content_type 추가
        data['content_id'] = content_id      # URL에서 받은 content_id 추가
        
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        if content_type == Like.ARTICLE:
            content_exists = Article.objects.filter(id=content_id).exists()
        elif content_type == Like.COMMENT:
            content_exists = Comment.objects.filter(id=content_id).exists()
        else:
            content_exists = False

        if not content_exists:
            raise serializers.ValidationError("컨텐츠가 존재하지 않습니다.")

        # 이미 좋아요를 눌렀는지 확인
        if Like.objects.filter(content_type=content_type, content_id=content_id, user=user).exists():
            raise serializers.ValidationError("이미 좋아요를 눌렀습니다.")

        # 중복이 없을 때만 생성
        like = Like.objects.create(content_type=content_type, content_id=content_id, user=user)
        
        serializer = self.serializer_class(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        # serializer = self.serializer_class(data=request.data)
        # serializer.is_valid(raise_exception=True)

        # content_type = serializer.validated_data['content_type']
        # content_id = serializer.validated_data['content_id']
        # user = request.user

        # if content_type == Like.ARTICLE:
        #     content = Article.objects.filter(id=content_id).exists()
        # elif content_type == Like.COMMENT:
        #     content = Comment.objects.filter(id=content_id).exists()
        # else:
        #     content = False

        # if not content:
        #     raise serializers.ValidationError("Content does not exist.")

        # like, created = Like.objects.get_or_create(content_type=content_type, content_id=content_id, user=user)

        # if not created:
        #     raise serializers.ValidationError("You have already liked this content.")
        
        # serializer.save(user=user)
        # return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, content_type, content_id):
        user = request.user

        try:
            like = Like.objects.get(content_type=content_type, content_id=content_id, user=user)
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({"detail": "Like not found."}, status=status.HTTP_404_NOT_FOUND)

    
class SubscriptionView(APIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # 구독 목록 조회
        subscriptions = Subscription_test.objects.filter(subscriber=request.user)
        serializer = self.serializer_class(subscriptions, many=True)
        return Response(serializer.data)

    def post(self, request, article_pk):
        # 게시글 작성자 구독 처리
        try:
            article = Article.objects.get(pk=article_pk)
        except Article.DoesNotExist:
            return Response({"detail": "게시물을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        subscribed_to = article.user

        # 이미 구독 중인지 확인
        if Subscription_test.objects.filter(subscriber=request.user, subscribed_to=subscribed_to).exists():
            return Response({"detail": "이미 구독 중입니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 구독 생성
        Subscription_test.objects.create(subscriber=request.user, subscribed_to=subscribed_to)
        return Response({"detail": "구독 성공!"}, status=status.HTTP_201_CREATED)
        
        
        
        
# class LikeCreateView(generics.CreateAPIView):
#     serializer_class = LikeSerializer

#     def perform_create(self, serializer):
#         content_type = serializer.validated_data['content_type']
#         content_id = serializer.validated_data['content_id']
#         user = self.request.user

#         # Check if content exists
#         if content_type == Like.ARTICLE:
#             content = Article.objects.filter(id=content_id).exists()
#         elif content_type == Like.COMMENT:
#             content = Comment.objects.filter(id=content_id).exists()
#         else:
#             content = False
        
#         if not content:
#             raise serializers.ValidationError("Content does not exist.")

#         # Save like
#         serializer.save(user=user)

# class DislikeView(generics.DestroyAPIView):
#     queryset = Like.objects.all()

#     def delete(self, request, *args, **kwargs):
#         content_type = self.kwargs['content_type']
#         content_id = self.kwargs['content_id']
#         user = request.user

#         try:
#             like = Like.objects.get(content_type=content_type, content_id=content_id, user=user)
#             like.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Like.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

  
        
# class SubscriptionCreateView(generics.CreateAPIView):
#     serializer_class = SubscriptionSerializer
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         article = Article.objects.get(pk=self.kwargs['article_pk'])
#         subscribed_to = article.user

#         # 이미 구독 중인지 확인
#         if Subscription.objects.filter(subscriber=request.user, subscribed_to=subscribed_to).exists():
#             return Response({"detail": "You are already subscribed to this user."}, status=status.HTTP_400_BAD_REQUEST)

#         # 구독 생성
#         Subscription.objects.create(subscriber=request.user, subscribed_to=subscribed_to)
#         return Response({"detail": "Subscription successful!"}, status=status.HTTP_201_CREATED)
    
# # 좋아요 목록 조회
# class LikeListView(generics.ListAPIView):
#     serializer_class = LikeSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         content_id = self.kwargs.get('content_id')
#         request_path = self.request.path

#         if 'articles' in request_path:
#             content_type = Like.ARTICLE
#         elif 'comments' in request_path:
#             content_type = Like.COMMENT
#         else:
#             content_type = None

#         if content_type:
#             queryset = Like.objects.filter(content_type=content_type, content_id=content_id)
#         else:
#             queryset = Like.objects.none()
        
#         return queryset
    
# # 구독자 목록 조회
# class SubscriptionListView(generics.ListAPIView):
#     serializer_class = SubscriptionSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Subscription.objects.filter(subscriber=self.request.user)


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