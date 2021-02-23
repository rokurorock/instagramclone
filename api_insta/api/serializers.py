from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile, Post, Comment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()  # カスタマイズしたUserモデルを取得
        fields = ('id', 'email', 'password')  # シリアライザーで利用したいパラメーター
        # write_onlyやread_onlyなどの属性を決定。クライアントからreadできないようにしたい
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):  # validated_data バリデーションに問題なければ辞書型でfieldの内容が入ってくる
        user = get_user_model().objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(
        format="%Y-%m-%d", read_only=True)  # 人が読みやすい日付形式に変更

    class Meta:
        model = Profile
        fields = ('id', 'nickName', 'userProfile', 'created_on', 'img')
        # クライアントからwriteできないようにする？
        extra_kwargs = {'userProfile': {'read_only': True}}


class PostSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'userPost', 'created_on', 'img', 'liked')
        extra_kwargs = {'userPost': {'read_only': True}}


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'userComment', 'post')
        # views.pyでログインしているユーザーを自動で割り当てるからread_only
        extra_kwargs = {'userComment': {'read_only': True}}


# 参照
# 公式サイト　https://www.django-rest-framework.org/api-guide/serializers/
