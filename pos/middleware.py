from django.shortcuts import redirect
from django.urls import reverse

class AdminRoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs que requieren rol de administrador
        admin_urls = ['/pos/admin/', '/admin_dashboard/', '/admin_ventas/', '/admin_productos/', '/admin_config/']
        
        # Si el usuario está autenticado y trata de acceder a URLs de admin
        if request.user.is_authenticated and any(request.path.startswith(url) for url in admin_urls):
            if request.user.rol != 'administrador':
                # Redirigir al POS si es empleado
                return redirect('pos:pos')
        
        response = self.get_response(request)
        return response
