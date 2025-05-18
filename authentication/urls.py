# authentication/urls.py

from django.urls import path
from .views import ChukaiLoginView, BaibaiLoginView, BaibaiLoginApiView, ChukaiLoginAPIView

app_name = 'authentication'

urlpatterns = [
    # 仲介アプリ用ログイン
    path('chukai/login/', ChukaiLoginView.as_view(), name='chukai_login'),
    # 売買アプリ用ログイン
    path('baibai/login/', BaibaiLoginView.as_view(), name='baibai_login'),
    path(
        'baibai/login/api/',
        BaibaiLoginApiView.as_view(),
        name='baibai_login_api'   # ← テンプレートの `{% url 'authentication:baibai_login_api' %}` と一致
    ),
    path(
        'chukai/login/api/',
        ChukaiLoginAPIView.as_view(),
        name='chukai_login_api'   # ← テンプレートの `{% url 'authentication:baibai_login_api' %}` と一致
    ),
    
]

