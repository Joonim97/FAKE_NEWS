import sys, os, ollama # 추후 accounts 추가 되고 마이그레이션 한 후 가동해봤을 때 서버 중단 작동하지 않으면 os.quit 로 교체하도록
from rest_framework import generics
from rest_framework.response import Response
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
        title, description = self.generator(topic).split("\n", 1)

        # Article 데이터로 저장, 현재 사용자 할당
        article_data = {
            "title": title.strip(),
            "description": description.strip(),
            "isFake": "FAKE",
        }

        serializer = self.get_serializer(data=article_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=201)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    