from django.db import models
from accounts.models import User

# 기사 모델
class Article(models.Model):
    FAKE_CHOICES = [
        ('REAL', '진짜'),
        ('FAKE', '가짜'),
        ('UNKNOWN', '알수없음'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    isFake = models.CharField(max_length=10, choices=FAKE_CHOICES, default='UNKNOWN')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# 댓글 모델
class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)  # 특정 기사에 종속 (기사 id 대입)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:20]
