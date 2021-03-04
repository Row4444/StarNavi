from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

User = get_user_model()


class UpdateLastActivityMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user and request.user.is_authenticated:
            User.objects.filter(id=request.user.id).update(last_activity=timezone.now())

