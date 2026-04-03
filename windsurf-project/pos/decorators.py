from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def admin_required(view_func):
    """
    Decorador que requiere que el usuario sea administrador
    """
    @login_required
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.rol != 'administrador':
            return redirect('pos:pos')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def employee_or_admin_required(view_func):
    """
    Decorador que permite acceso tanto a empleados como administradores
    """
    @login_required
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.rol not in ['empleado', 'administrador']:
            return redirect('pos:login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
