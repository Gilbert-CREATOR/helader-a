from django.urls import path
from . import views

app_name = 'pos'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # POS principal
    path('pos/', views.pos_view, name='pos'),
    
    # AJAX endpoints
    path('buscar-productos/', views.buscar_productos, name='buscar_productos'),
    path('agregar-al-carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('actualizar-carrito/', views.actualizar_carrito, name='actualizar_carrito'),
    path('vaciar-carrito/', views.vaciar_carrito, name='vaciar_carrito'),
    path('procesar-venta/', views.procesar_venta, name='procesar_venta'),
    
    # Tickets
    path('ticket/<int:venta_id>/', views.ticket_view, name='ticket'),
    
    # Panel de administración
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/ventas/', views.admin_ventas, name='admin_ventas'),
    path('admin/productos/', views.admin_productos, name='admin_productos'),
    path('admin/productos/eliminar/<int:producto_id>/', views.admin_eliminar_producto, name='admin_eliminar_producto'),
    path('admin/categorias/', views.admin_categorias, name='admin_categorias'),
    path('admin/categorias/eliminar/<int:categoria_id>/', views.admin_eliminar_categoria, name='admin_eliminar_categoria'),
    path('admin/config/', views.admin_config, name='admin_config'),
    path('admin/config/eliminar/<int:usuario_id>/', views.admin_eliminar_usuario, name='admin_eliminar_usuario'),
]
