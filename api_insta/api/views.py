from rest_framework import generics
from rest_framework import viewsets
# デフォルトでsetting,pyでJWTの認証方式を通らないとViewを見れないようにするけど、ユーザーを作る段階ではユーザー情報がないので、それを許可するのがAllowAny
from rest_framework.permissions import AllowAny
from . import serializers
from .models import Profile, Post, Comment
# Create your views here.


# 汎用APIview　新規ユーザーを作ることを特化したviewのためCreateAPIViewを継承している
class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer  # 対象となるシリアライザーを指定
    permission_classes = (AllowAny,)  # 新規でユーざーを作る人は誰でもアクセスできるようにする必要がある


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()  # 新規作成とか更新をする必要があるからmodelviewsetを継承
    serializer_class = serializers.ProfileSerializer

    def perform_create(self, serializer):
        # 新規で作成する時にrequest.user(ログインしているユーザー)を取得して新規にユーザー情報を作成するという処理
        serializer.save(userProfile=self.request.user)


class MyProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    # ログインしているユーザーのプロフィールをこのviewにアクセスした時にresponseで返すようにする
    def get_queryset(self):
        return self.queryset.filter(userProfile=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

    def perform_create(self, serializer):
        # ポストを作る時ログインしているユーザーの情報を割り当てる
        serializer.save(userPost=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        # コメントを作る時ログインしているユーザーの情報を割り当てる
        serializer.save(userComment=self.request.user)
