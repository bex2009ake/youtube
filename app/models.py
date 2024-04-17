from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    bio = models.TextField()
    img = models.ImageField(upload_to='user/')


    def __str__(self) -> str:
        return self.username
    


class Video(models.Model):
    title = models.CharField(max_length=250)
    img = models.ImageField(upload_to='video_img/')
    video = models.FileField(upload_to='videos/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.ManyToManyField(User, related_name='views', blank=True)
    likes = models.ManyToManyField(User, related_name='like', blank=True)
    dislike = models.ManyToManyField(User, related_name='dislike', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)



    def add_like(self, user):
        self.likes.add(user)
        self.dislike.remove(user) if user in self.dislike.all() else None


    def add_dislike(self, user):
        self.dislike.add(user)
        self.likes.remove(user) if user in self.likes.all() else None


    def __str__(self) -> str:
        return self.title
    

class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    msg = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.owner.username
    

class Favorite(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    videos = models.ManyToManyField(Video, related_name='favorite', blank=True)

    def add(self, video):
        self.videos.add(video)

    def remove(self, video):
        self.videos.remove(video)

    
    def __str__(self) -> str:
        return str(self.user.pk)



class History(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    videos = models.ManyToManyField(Video, related_name='history', blank=True)

    def add(self, video):
        self.videos.add(video)

    def remove(self, video):
        self.videos.remove(video)

    
    def __str__(self) -> str:
        return str(self.user.pk)



# {
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxMjk4MzgwNCwiaWF0IjoxNzEyODk3NDA0LCJqdGkiOiJiZjkyMmViNzg0ZWU0ZTYzYmI3YTk0ZGI3N2NmNmFiNCIsInVzZXJfaWQiOjN9.5qS3kylUGt7ZyxnIP0vRvDFgCkqaDWs5nkLm6Rc0_Rc",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEyODk4MDA0LCJpYXQiOjE3MTI4OTc0MDQsImp0aSI6Ijk2MWUzMmZkZTE3NjQyZDA4YThhNjkyNzZiZTc3NzRmIiwidXNlcl9pZCI6M30.xnbUHdDgbnTMXHi62d4V1UJdT8DpMX1rlcOc5k6nFmY"
# }
