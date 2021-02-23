from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'user'

# REST APIの場合routerを使ってviewとパスを紐づける(view.setで継承したもの)
router = DefaultRouter()
router.register('profile', views.ProfileViewSet)
router.register('post', views.PostViewSet)
router.register('comment', views.CommentViewSet)

# 汎用viewと紐づける場合はこちら(geneticを継承したもの)
urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('myprofile/', views.MyProfileListView.as_view(), name='myprofile'),
    path('', include(router.urls))  # ルートのパスに来た時routerのパスを読みにいくようにしている
]
