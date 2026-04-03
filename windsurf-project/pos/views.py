from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Sum, Count, Q
from django.core.paginator import Paginator
from decimal import Decimal
import json
from datetime import datetime, timedelta

from .models import Producto, Venta, DetalleVenta, Categoria, Usuario
from .decorators import admin_required, employee_or_admin_required
from .forms import UsuarioForm, ProductoForm, CategoriaForm

def login_view(request):
    if request.user.is_authenticated:
        if request.user.rol == 'administrador':
            return redirect('pos:admin_dashboard')
        else:
            return redirect('pos:pos')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.rol == 'administrador':
                return redirect('pos:admin_dashboard')
            else:
                return redirect('pos:pos')
        else:
            error = "Usuario o contraseña incorrectos"
            return render(request, 'pos/login.html', {'error': error})
    
    return render(request, 'pos/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('pos:login')

@login_required
def pos_view(request):
    if request.user.rol != 'empleado':
        return redirect('pos:admin_dashboard')
    
    productos = Producto.objects.filter(activo=True, stock__gt=0).order_by('categoria', 'nombre')
    categorias = Categoria.objects.all()
    
    context = {
        'productos': productos,
        'categorias': categorias,
    }
    return render(request, 'pos/pos.html', context)

@login_required
def buscar_productos(request):
    query = request.GET.get('q', '')
    productos = Producto.objects.filter(
        Q(nombre__icontains=query) | Q(tipo__icontains=query),
        activo=True,
        stock__gt=0
    ).order_by('nombre')[:10]
    
    data = []
    for producto in productos:
        data.append({
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': float(producto.precio),
            'stock': producto.stock,
            'tipo': producto.get_tipo_display(),
        })
    
    return JsonResponse({'productos': data})

@csrf_exempt
@login_required
@require_POST
def agregar_al_carrito(request):
    try:
        data = json.loads(request.body)
        producto_id = data.get('producto_id')
        cantidad = data.get('cantidad', 1)
        
        producto = get_object_or_404(Producto, id=producto_id, activo=True)
        
        if producto.stock < cantidad:
            return JsonResponse({
                'success': False,
                'error': f'Stock insuficiente. Solo hay {producto.stock} unidades disponibles.'
            })
        
        carrito = request.session.get('carrito', [])
        
        # Buscar si el producto ya está en el carrito
        item_encontrado = None
        for item in carrito:
            if item['producto_id'] == producto_id:
                item_encontrado = item
                break
        
        if item_encontrado:
            nueva_cantidad = item_encontrado['cantidad'] + cantidad
            if producto.stock < nueva_cantidad:
                return JsonResponse({
                    'success': False,
                    'error': f'Stock insuficiente. Solo hay {producto.stock} unidades disponibles.'
                })
            item_encontrado['cantidad'] = nueva_cantidad
            item_encontrado['subtotal'] = float(producto.precio * nueva_cantidad)
        else:
            carrito.append({
                'producto_id': producto.id,
                'nombre': producto.nombre,
                'precio': float(producto.precio),
                'cantidad': cantidad,
                'subtotal': float(producto.precio * cantidad),
                'tipo': producto.get_tipo_display(),
            })
        
        request.session['carrito'] = carrito
        
        # Calcular totales
        total = sum(item['subtotal'] for item in carrito)
        total_items = sum(item['cantidad'] for item in carrito)
        
        return JsonResponse({
            'success': True,
            'carrito': carrito,
            'total': total,
            'total_items': total_items,
            'message': f'{producto.nombre} agregado al carrito'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@login_required
@require_POST
def actualizar_carrito(request):
    try:
        data = json.loads(request.body)
        producto_id = data.get('producto_id')
        cantidad = data.get('cantidad', 0)
        
        carrito = request.session.get('carrito', [])
        
        if cantidad == 0:
            # Eliminar del carrito
            carrito = [item for item in carrito if item['producto_id'] != producto_id]
        else:
            # Actualizar cantidad
            producto = get_object_or_404(Producto, id=producto_id, activo=True)
            
            if producto.stock < cantidad:
                return JsonResponse({
                    'success': False,
                    'error': f'Stock insuficiente. Solo hay {producto.stock} unidades disponibles.'
                })
            
            for item in carrito:
                if item['producto_id'] == producto_id:
                    item['cantidad'] = cantidad
                    item['subtotal'] = float(producto.precio * cantidad)
                    break
        
        request.session['carrito'] = carrito
        
        # Calcular totales
        total = sum(item['subtotal'] for item in carrito)
        total_items = sum(item['cantidad'] for item in carrito)
        
        return JsonResponse({
            'success': True,
            'carrito': carrito,
            'total': total,
            'total_items': total_items
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@login_required
@require_POST
def vaciar_carrito(request):
    request.session['carrito'] = []
    return JsonResponse({
        'success': True,
        'carrito': [],
        'total': 0,
        'total_items': 0
    })

@csrf_exempt
@login_required
@require_POST
def procesar_venta(request):
    try:
        carrito = request.session.get('carrito', [])
        
        if not carrito:
            return JsonResponse({
                'success': False,
                'error': 'El carrito está vacío'
            })
        
        # Verificar stock antes de procesar
        for item in carrito:
            producto = Producto.objects.get(id=item['producto_id'])
            if producto.stock < item['cantidad']:
                return JsonResponse({
                    'success': False,
                    'error': f'Stock insuficiente para {producto.nombre}. Solo hay {producto.stock} unidades disponibles.'
                })
        
        # Crear la venta
        total = sum(item['subtotal'] for item in carrito)
        venta = Venta.objects.create(
            usuario=request.user,
            total=total,
            metodo_pago='efectivo'
        )
        
        # Crear detalles y reducir stock
        for item in carrito:
            producto = Producto.objects.get(id=item['producto_id'])
            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=item['cantidad'],
                precio_unitario=item['precio'],
                subtotal=item['subtotal']
            )
            producto.reducir_stock(item['cantidad'])
        
        # Vaciar carrito
        request.session['carrito'] = []
        
        return JsonResponse({
            'success': True,
            'venta_id': venta.id,
            'total': float(venta.total),
            'message': 'Venta procesada exitosamente'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def ticket_view(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = venta.detalles.all()
    
    context = {
        'venta': venta,
        'detalles': detalles,
    }
    return render(request, 'pos/ticket.html', context)

@admin_required
def admin_dashboard(request):
    today = timezone.now().date()
    
    # Estadísticas del día
    ventas_hoy = Venta.objects.filter(fecha__date=today, cancelada=False)
    total_ventas_hoy = ventas_hoy.aggregate(Sum('total'))['total__sum'] or 0
    cantidad_ventas_hoy = ventas_hoy.count()
    
    # Estadísticas del mes
    month_start = today.replace(day=1)
    ventas_mes = Venta.objects.filter(fecha__date__gte=month_start, cancelada=False)
    total_ventas_mes = ventas_mes.aggregate(Sum('total'))['total__sum'] or 0
    cantidad_ventas_mes = ventas_mes.count()
    
    # Productos más vendidos
    productos_mas_vendidos = DetalleVenta.objects.filter(
        venta__fecha__date__gte=month_start,
        venta__cancelada=False
    ).values('producto__nombre').annotate(
        total_vendido=Sum('cantidad'),
        total_ingresos=Sum('subtotal')
    ).order_by('-total_vendido')[:10]
    
    # Ventas recientes
    ventas_recientes = Venta.objects.filter(cancelada=False).order_by('-fecha')[:10]
    
    context = {
        'total_ventas_hoy': total_ventas_hoy,
        'cantidad_ventas_hoy': cantidad_ventas_hoy,
        'total_ventas_mes': total_ventas_mes,
        'cantidad_ventas_mes': cantidad_ventas_mes,
        'productos_mas_vendidos': productos_mas_vendidos,
        'ventas_recientes': ventas_recientes,
    }
    
    return render(request, 'pos/admin_dashboard.html', context)

@admin_required
def admin_ventas(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    
    ventas = Venta.objects.filter(cancelada=False).order_by('-fecha')
    
    if fecha_inicio:
        ventas = ventas.filter(fecha__date__gte=fecha_inicio)
    if fecha_fin:
        ventas = ventas.filter(fecha__date__lte=fecha_fin)
    
    paginator = Paginator(ventas, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Totales
    total_ventas = ventas.aggregate(Sum('total'))['total__sum'] or 0
    cantidad_ventas = ventas.count()
    
    context = {
        'page_obj': page_obj,
        'total_ventas': total_ventas,
        'cantidad_ventas': cantidad_ventas,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    }
    
    return render(request, 'pos/admin_ventas.html', context)

@admin_required
def admin_productos(request):
    if request.method == 'POST':
        # Determinar si es crear o editar
        producto_id = request.POST.get('producto_id')
        
        if producto_id:
            # Editar producto existente
            producto = get_object_or_404(Producto, id=producto_id)
            form = ProductoForm(request.POST, instance=producto)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True, 'message': 'Producto actualizado correctamente'})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
        else:
            # Crear nuevo producto
            form = ProductoForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True, 'message': 'Producto creado correctamente'})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
    
    # GET request - mostrar lista
    productos = Producto.objects.all().order_by('categoria', 'nombre')
    categorias = Categoria.objects.all()
    
    # Calcular estadísticas
    productos_activos = productos.filter(activo=True).count()
    stock_bajo_productos = [p for p in productos if p.stock <= 5]
    
    context = {
        'productos': productos,
        'categorias': categorias,
        'productos_activos': productos_activos,
        'stock_bajo_productos': stock_bajo_productos,
    }
    
    return render(request, 'pos/admin_productos.html', context)

@admin_required
def admin_eliminar_producto(request, producto_id):
    if request.method == 'DELETE':
        producto = get_object_or_404(Producto, id=producto_id)
        nombre_producto = producto.nombre
        producto.delete()
        return JsonResponse({
            'success': True, 
            'message': f'Producto "{nombre_producto}" eliminado correctamente'
        })
    else:
        return JsonResponse({'success': False, 'message': 'Método no permitido'})

@admin_required
def admin_categorias(request):
    if request.method == 'POST':
        categoria_id = request.POST.get('categoria_id')
        
        if categoria_id:
            # Editar categoría existente
            categoria = get_object_or_404(Categoria, id=categoria_id)
            form = CategoriaForm(request.POST, instance=categoria)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True, 'message': 'Categoría actualizada correctamente'})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
        else:
            # Crear nueva categoría
            form = CategoriaForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True, 'message': 'Categoría creada correctamente'})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@admin_required
def admin_eliminar_categoria(request, categoria_id):
    if request.method == 'DELETE':
        categoria = get_object_or_404(Categoria, id=categoria_id)
        
        # Verificar si hay productos asociados
        productos_asociados = categoria.producto_set.count()
        if productos_asociados > 0:
            return JsonResponse({
                'success': False, 
                'message': f'No se puede eliminar la categoría "{categoria.nombre}" porque tiene {productos_asociados} productos asociados'
            })
        
        nombre_categoria = categoria.nombre
        categoria.delete()
        return JsonResponse({
            'success': True, 
            'message': f'Categoría "{nombre_categoria}" eliminada correctamente'
        })
    else:
        return JsonResponse({'success': False, 'message': 'Método no permitido'})

@admin_required
def admin_config(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        
        if usuario_id:
            # Editar usuario existente
            usuario = get_object_or_404(Usuario, id=usuario_id)
            form = UsuarioForm(request.POST, instance=usuario)
            if form.is_valid():
                # Si se proporciona contraseña, actualizarla
                if request.POST.get('password'):
                    usuario.set_password(request.POST['password'])
                form.save()
                return JsonResponse({'success': True, 'message': 'Usuario actualizado correctamente'})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
        else:
            # Crear nuevo usuario
            form = UsuarioForm(request.POST)
            if form.is_valid():
                usuario = form.save(commit=False)
                # Establecer contraseña
                if request.POST.get('password'):
                    usuario.set_password(request.POST['password'])
                usuario.save()
                return JsonResponse({'success': True, 'message': 'Usuario creado correctamente'})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
    
    # GET request
    usuarios = Usuario.objects.all().order_by('rol', 'username')
    
    context = {
        'usuarios': usuarios,
    }
    
    return render(request, 'pos/admin_config.html', context)

@admin_required
def admin_eliminar_usuario(request, usuario_id):
    if request.method == 'DELETE':
        usuario = get_object_or_404(Usuario, id=usuario_id)
        
        # Proteger al usuario admin principal
        if usuario.username == 'admin':
            return JsonResponse({
                'success': False, 
                'message': 'No se puede eliminar al usuario administrador principal'
            })
        
        nombre_usuario = usuario.username
        usuario.delete()
        return JsonResponse({
            'success': True, 
            'message': f'Usuario "{nombre_usuario}" eliminado correctamente'
        })
    else:
        return JsonResponse({'success': False, 'message': 'Método no permitido'})
