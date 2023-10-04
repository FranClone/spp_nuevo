from functools import wraps
from django.shortcuts import render

def require_role(roles_required):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.roles in roles_required:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, 'dashboard.html')
        return _wrapped_view
    return decorator

            