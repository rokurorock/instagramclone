
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
# Create your models here.


def upload_avatar_path(instance, filename):  # filenameはユーザーが保存しようとした画像ファイルの名前
    ext = filename.split('.')[-1]
    return '/'.join(['avatars', str(instance.userProfile.id)+str(instance.nickName)+str(".")+str(ext)])


def upload_post_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['posts', str(instance.userPost.id)+str(instance.title)+str(".")+str(ext)])


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):  # ユーザーを作る時にemailを利用するように変更
        if not email:
            raise ValueError('email is must')

        user = self.model(email=self.normalize_email(email)
                          )  # emailを正規化　大文字→小文字など
        user.set_password(password)  # ハッシュ化してパスワードを保存
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()  # ネストすることでユーザークラスのインスタンスからUserManager()クラスの間数を呼び出すことができるようになる

    USERNAME_FIELD = 'email'  # ユーザーをemailに変更

    def __str__(self):
        return self.email


class Profile(models.Model):
    nickName = models.CharField(max_length=20)
    userProfile = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='userProfile',
        on_delete=models.CASCADE  # 参照しているユーザーが削除されると対象としているプロフィールも削除されるようになる
    )
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True,
                            upload_to=upload_avatar_path)  # upload_toは画像を保存するパスを指定する

    def __str__(self):
        return self.nickName


class Post(models.Model):  # 投稿した情報のクラス
    title = models.CharField(max_length=100)
    userPost = models.ForeignKey(  # oneTOmanyはForeignKeyを使う
        settings.AUTH_USER_MODEL, related_name='userPost',
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_post_path)
    liked = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='liked', blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):  # コメントのクラス
    text = models.CharField(max_length=100)
    userComment = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='userComment',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
