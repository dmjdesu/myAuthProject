# authentication/urls.py

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import LogoutView, UserStatusView, APITestView

app_name = 'authentication'

urlpatterns = [
    # ① ユーザー名/パスワードでトークン発行
    path('token/',         TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # ② リフレッシュで access トークン再発行
    path('token/refresh/', TokenRefreshView.as_view(),     name='token_refresh'),
    # ③ Blacklist 方式のログアウト
    path('logout/',        LogoutView.as_view(),           name='logout'),
    # ④ 認証済ユーザー情報取得
    path('user/',          UserStatusView.as_view(),       name='user_status'),
    # ⑤ テスト用ページ
    path('test/',          APITestView.as_view(),          name='api_test'),
]
