from functools import wraps
from django.shortcuts import render

def require_role(rol):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.roles == rol:
                return view_func(request, *args, **kwargs)
            else:
                #alert_message = None
                #return render(request, 'aviso.html')  # Página de error de permisos
                #alert_message = "Usted no tiene los permisos para ingresar al servicio solicitado."
                #return render(request, 'aviso.html', {'alert_message': alert_message})
                return render(request, 'dashboard.html')
        return _wrapped_view
    return decorator
            