from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from oauth2_provider.models import Application

User = get_user_model()

class Command(BaseCommand):
    help = '仲介・売買用の OAuth2 クライアントを作成します'

    def handle(self, *args, **options):
        admin = User.objects.filter(is_superuser=True).first()
        if not admin:
            self.stdout.write(self.style.ERROR('スーパーユーザーが見つかりません'))
            return

        clients = [
            {
                'name': 'Chukai Client',
                'client_id': 'chukai_client_id',
                'client_secret': 'chukai_secret',
                'redirect_uris': 'https://chukai.example.com/auth/callback/',
            },
            {
                'name': 'Baibai Client',
                'client_id': 'baibai_client_id',
                'client_secret': 'baibai_secret',
                'redirect_uris': 'https://baibai.example.com/auth/callback/',
            },
        ]

        for cfg in clients:
            app, created = Application.objects.get_or_create(
                name=cfg['name'],
                defaults={
                    'user': admin,
                    'client_id': cfg['client_id'],
                    'client_secret': cfg['client_secret'],
                    'client_type': Application.CLIENT_CONFIDENTIAL,
                    'authorization_grant_type': Application.GRANT_AUTHORIZATION_CODE,
                    'redirect_uris': cfg['redirect_uris'],
                    'skip_authorization': False,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"作成: {app.name}"))
            else:
                self.stdout.write(f"既存: {app.name} (client_id={app.client_id})")
