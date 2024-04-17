from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from app.models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer
# Create your views here.

class VideoApi(ModelSerializer):
    class Meta:
        model = Video
        fields = ['title', 'img', 'author', 'video']


class Singup(APIView):
    def get(self, req: Request):
        return Response({'msg': 'Singup'})
    
    def post(self, req: Request):
        name = req.data.get('username')
        password = req.data.get('password')
        bio = req.data.get('bio')
        img = req.data.get('img')

        user = User.objects.create_user(username=name, password=password, bio=bio, img=img)
        token = RefreshToken.for_user(user)

        Favorite.objects.create(user=user)
        History.objects.create(user=user)

        return Response({
            'refresh': str(token),
            'access': str(token.access_token)
        })
    

class Singin(APIView):
    def get(self, req: Request):
        return Response({'msg': 'Singin'})
    
    def post(self, req: Request):
        name = req.data.get('username')
        password = req.data.get('password')


        user = User.objects.filter(username=name).first()
        if not bool(user):
            return Response({'err': 'User doesn`t exist'})
        

        if not check_password(password, user.password):
            return Response({'err': 'Wrong password'})
        token = RefreshToken.for_user(user)

        return Response({
            'refresh': str(token),
            'access': str(token.access_token)
        })
    

class VideoCreateRead(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, req: Request):
        title = req.query_params.get('title', None)
        date = req.query_params.get('date', None)
        views = req.query_params.get('views', None)

        db = Video.objects.all()  
        if title:
            db = db.filter(title__icontains=title)
        
        if date:
            db = db.order_by(date)

        if views:
            db = db.order_by(views)

        return Response({'data': db.values()})
    

    def post(self, req: Request):
        title = req.data.get('title')
        img = req.data.get('img')
        video = req.FILES.get('video')


        try:
            author = req.user
            video_obj = Video.objects.create(title=title, img=img, video=video, author=author)
            serializer = VideoApi(video_obj)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)})


class DeleteVideo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, req: Request, pk):
        return Response({'msg': 'Delete video'})
    
    def post(self, req: Request, pk):
        video = Video.objects.filter(pk=pk).first()

        if video.author == req.user:
            video.delete()
            return Response({'deleted': True})
        return Response({'err': True})
    

class LikesViewsVideo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, req: Request, pk):
        video = Video.objects.filter(pk=pk).first()
        if not video.views.filter(id=req.user.id).exists():
            video.views.add(req.user)
            video.save()
            return Response({'views': video.views.count()})
        return Response({'views': video.views.count()})
    
    def post(self, req: Request, pk):
        action = req.data.get('action')
        video = Video.objects.filter(pk=pk).first()

        if action == 'like':
            if not video.likes.filter(id=req.user.id).exists():
                video.likes.add(req.user)
                video.save()
                if video.dislike.filter(id=req.user.id).exists():
                    video.dislike.remove(req.user)
                    video.save()
                return Response({'like': video.likes.count()})
            return Response({'like': video.likes.count()})
        
        if action == 'dislike':
            if not video.dislike.filter(id=req.user.id).exists():
                video.dislike.add(req.user)
                video.save()
                if video.likes.filter(id=req.user.id).exists():
                    video.likes.remove(req.user)
                    video.save()
                return Response({'dislike': video.dislike.count()})
            return Response({'dislike': video.dislike.count()})
        
        return Response({'err': True})


class CommentCreateRead(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, req: Request, pk):
        video = Video.objects.all().filter(pk=pk).first()
        comments = Comment.objects.all().filter(video=video).values()

        return Response({'data': comments})
    

    def post(self, req: Request, pk):
        video = Video.objects.all().filter(pk=pk).first()
        comment = Comment.objects.create(owner=req.user, video=video, msg=req.data.get('msg'))

        return Response({'msg': comment.msg})
    



class HistoryCreateRead(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, req: Request, pk):

        return Response({'data': 'history'})
    

    def post(self, req: Request, pk):
        video = Video.objects.all().filter(pk=pk).first()
        history = History.objects.create(user=req.user, video=video)

        return Response({'data': history.user.username})
    


class HistoryRead(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, req: Request):
        history = History.objects.all().filter(user=req.user).values()

        return Response({'data': history})
    

class FavoriteCreateRead(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, req: Request, pk):

        return Response({'data': 'favorite'})
    

    def post(self, req: Request, pk):
        video = Video.objects.all().filter(pk=pk).first()
        favorite = Favorite.objects.create(user=req.user, video=video)

        return Response({'data': favorite.user.username})
    


class FavoriteRead(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, req: Request):
        favorite = Favorite.objects.all().filter(user=req.user).values()

        return Response({'data': favorite})
    
