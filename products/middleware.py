from .models import PageView

class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Логируем только GET-запросы
        if request.method == 'GET' and not request.path.startswith('/admin'):
            PageView.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_id=request.session.session_key,
                url=request.build_absolute_uri(),
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip