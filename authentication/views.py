from django.contrib.auth.views import LoginView
from .forms import ChukaiLoginForm, BaibaiLoginForm
from django.urls import reverse
from urllib.parse import urlencode

from django.shortcuts import render
from oauth2_provider.views import AuthorizationView
from oauth2_provider.models import get_application_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

Application = get_application_model()

@method_decorator(login_required, name='dispatch')
class CheckedAuthorizationView(AuthorizationView):
    """
    OAuth2 認可前に「ユーザーがこのアプリケーションで
    アカウントを持っているか」をチェックします。
    """
    def dispatch(self, request, *args, **kwargs):
        client_id = request.GET.get('client_id')
        try:
            app = Application.objects.get(client_id=client_id)
        except Application.DoesNotExist:
            return render(request, 'authentication/error.html', {
                'error': 'Unknown client_id.'
            }, status=400)
        # ❶ ここでユーザーが allowed_applications に含まれているかチェック
        if not request.user.allowed_applications.filter(pk=app.pk).exists():
            return render(request, 'authentication/error.html', {
                'error': f"あなたは「{app.name}」のアカウントを持っていません。"
            }, status=403)

        # 問題なければ通常の認可処理へ
        return super().dispatch(request, *args, **kwargs)


class ChukaiLoginView(LoginView):
    form_class    = ChukaiLoginForm
    template_name = 'authentication/chukai_login.html'
    # 認可サーバーに登録した chukai の client_id
    CLIENT_ID = 'chukai_client_id'

    def get_initial(self):
        init = super().get_initial() or {}
        # hidden field に client_id を埋め込む
        init['client_id'] = self.CLIENT_ID
        return init

    def get_success_url(self):
        # 認可サーバーの /o/authorize/ へ、client_id を渡してリダイレクト
        params = {
            'response_type': 'code',
            'client_id':     self.CLIENT_ID,
            'redirect_uri':  'https://chukai.example.com/auth/callback/',
            # 必要なら scope, state なども追加
        }
        return reverse('oauth2_provider:authorize') + '?' + urlencode(params)

class BaibaiLoginView(LoginView):
    form_class    = BaibaiLoginForm
    template_name = 'authentication/baibai_login.html'
    CLIENT_ID = 'baibai_client_id'

    def get_initial(self):
        init = super().get_initial() or {}
        init['client_id'] = self.CLIENT_ID
        return init

    def get_success_url(self):
        params = {
            'response_type': 'code',
            'client_id':     self.CLIENT_ID,
            'redirect_uri':  'https://baibai.example.com/auth/callback/',
        }
        return reverse('oauth2_provider:authorize') + '?' + urlencode(params)
# authentication/views.py

import json
from urllib.parse import urlencode

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie


class BaseLoginApiView(View):
    CLIENT_ID    = None
    REDIRECT_URI = None
    RESPONSE_TYPE= 'code'
    SCOPE        = 'read write'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        # 1) JSON のときだけ body を一度読み込んでキャッシュ
        ct = request.META.get('CONTENT_TYPE', '')
        if ct.startswith('application/json'):
            try:
                request.json_payload = json.loads(request.body.decode())
            except json.JSONDecodeError:
                request.json_payload = {}
        else:
            request.json_payload = None
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # 2) JSON 送信なら dispatch() のキャッシュを、そうでなければ request.POST を使う
        if request.json_payload is not None:
            data = request.json_payload
        else:
            data = request.POST

        username  = data.get('username')
        password  = data.get('password')
        client_id = data.get('client_id') or self.CLIENT_ID

        if not (username and password and client_id):
            return JsonResponse({'errors': ['必要なフィールドが不足しています。']}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is None:
            return JsonResponse({'errors': ['ユーザー名またはパスワードが正しくありません。']}, status=400)

        login(request, user)

        params = {
            'response_type': self.RESPONSE_TYPE,
            'client_id':     client_id,
            'redirect_uri':  self.REDIRECT_URI,
            'scope':         self.SCOPE,
        }
        authorize_url = reverse('oauth2_provider:authorize') + '?' + urlencode(params)
        return JsonResponse({'redirect': authorize_url})


class ChukaiLoginAPIView(BaseLoginApiView):
    CLIENT_ID    = 'chukai_client_id'
    REDIRECT_URI = 'https://chukai.example.com/auth/callback/'


class BaibaiLoginApiView(BaseLoginApiView):
    CLIENT_ID    = 'baibai_client_id'
    REDIRECT_URI = 'https://baibai.example.com/auth/callback/'
