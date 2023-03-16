from admin_interface.models import Theme

class SetThemeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Obtener la empresa del usuario actual
        if request.user.is_authenticated:
            empresa = getattr(request.user.userprofile, 'rut_empresa', None)

            # Asignar el tema correspondiente a la empresa
            if empresa and empresa.rut_empresa == "10477088-6":
                theme = Theme.objects.get(name='SPP')
                request.session['theme'] = theme.pk
            elif empresa and empresa.rut_empresa == "4532156-8":
                theme = Theme.objects.get(name='Masisa')
                request.session['theme'] = theme.pk
            else:
                theme = Theme.objects.get(name='SPP')
                request.session['theme'] = theme.pk

        response = self.get_response(request)

        return response
