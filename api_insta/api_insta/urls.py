from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    # emailとパスワードをpostに入れるとjwtトークンを返すようにする
    path('authen/', include('djoser.urls.jwt')),
]

# 画像をプロジェクト直下のメディアをするときに、保存されたファイルをurlのパスから参照できるようにするために追加
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
