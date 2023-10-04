from functools import wraps
from django.shortcuts import render

def require_role(rol):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.roles == rol:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, 'login.html')  # Página de error de permisos
        return _wrapped_view
    return decorator
