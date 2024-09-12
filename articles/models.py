from django.db import models
# from accounts.models import User # accounts 앱 완성 전까지는 일시적으로 주석처리


from django.contrib.auth.models import AbstractUser

# 임시 User 모델
# runserver 되는지 확인하려고 넣은 모델임
# accounts 완성되면 위의 import User 주석 해제, 프로젝트의 settings.py 랑 urls.py 에서도 주석 해제할거 해제하고 이 파트 삭제함
class User(AbstractUser):
    name = models.CharField(max_length=100, null=True, blank=True)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)

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
