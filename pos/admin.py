from django.contrib import admin
from .models import Usuario, Categoria, Producto, Venta, DetalleVenta

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'rol', 'is_active', 'date_joined']
    list_filter = ['rol', 'is_active']
    search_fields = ['username', 'email']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'precio', 'stock', 'activo', 'categoria']
    list_filter = ['tipo', 'activo', 'categoria']
    search_fields = ['nombre']
    list_editable = ['precio', 'stock', 'activo']

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'fecha', 'total', 'metodo_pago', 'cancelada']
    list_filter = ['metodo_pago', 'cancelada', 'fecha']
    search_fields = ['usuario__username']
    readonly_fields = ['fecha', 'total']

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ['venta', 'producto', 'cantidad', 'precio_unitario', 'subtotal']
    list_filter = ['producto']
    search_fields = ['producto__nombre', 'venta__id']
    readonly_fields = ['subtotal']
