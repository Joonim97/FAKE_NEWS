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

    def perform_update(self, serializer):
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
            serializer.save()


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
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        article_id = self.kwargs['article_pk']
        return Comment.objects.filter(article_id=article_id)
    
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