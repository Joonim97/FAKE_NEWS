from django.db import models
from django.conf import settings
from accounts.models import User


# 기사 모델
class Article(models.Model):
    FAKE_CHOICES = [
        ('REAL', '진짜'),
        ('FAKE', '가짜'),
        ('UNKNOWN', '알수없음'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/', blank=True)
    isFake = models.CharField(
        max_length=10, choices=FAKE_CHOICES, default='UNKNOWN')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# 댓글 모델

class Comment(models.Model):
    article = models.ForeignKey(
        Article, related_name='comments', on_delete=models.CASCADE)  # 특정 기사에 종속 (기사 id 대입)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.text[:20]
    
    
class Like(models.Model):
    ARTICLE = 'article'
    COMMENT = 'comment'
    LIKE_CHOICES = [
        (ARTICLE, 'Article'),
        (COMMENT, 'Comment'),
    ]
    
    content_type = models.CharField(max_length=10, choices=LIKE_CHOICES)
    content_id = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('content_type', 'content_id', 'user')
        indexes = [
            models.Index(fields=['content_type', 'content_id']),
        ]

    def __str__(self):
        return f'{self.user} likes {self.content_type} {self.content_id}'
    

class Subscription_test(models.Model):
    subscriber = models.ForeignKey(User, related_name='subscriptions', on_delete=models.CASCADE)
    subscribed_to = models.ForeignKey(User, related_name='subscribers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True) ## 마이그레이션하게 잠시 변경, auto_now_add 로 복구 예정

    class Meta:
        unique_together = ('subscriber', 'subscribed_to')

    def __str__(self):
        return f"{self.subscriber} subscribed to {self.subscribed_to}"
    