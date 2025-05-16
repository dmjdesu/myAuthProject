# authentication/views.py

# authentication/views.py

from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.generic import TemplateView


class LogoutView(APIView):
    """
    POST /auth/logout/
    { refresh } を受け取り、トークンを blacklist に登録してログアウト。
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        token = request.data.get('refresh')
        try:
            RefreshToken(token).blacklist()
            return Response(status=204)
        except Exception:
            return Response({'detail': '無効なトークンです'}, status=400)


class UserStatusView(APIView):
    """
    GET /auth/user/
    Authorization: Bearer <access> を検証し、
    認証ユーザー情報を返却。
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        return Response({
            'id':       user.id,
            'username': user.get_username(),
            'email':    user.email,
        })


class APITestView(TemplateView):
    """
    /auth/test/ にアクセスすると
    templates/authentication/test.html を返すだけのビュー
    """
    template_name = "authentication/test.html"
