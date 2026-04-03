from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from pos.models import Categoria, Producto

Usuario = get_user_model()

class Command(BaseCommand):
    help = 'Crear datos iniciales para el sistema POS'

    def handle(self, *args, **options):
        self.stdout.write('Creando datos iniciales...')
        
        # Crear usuarios
        self.crear_usuarios()
        
        # Crear categorías
        self.crear_categorias()
        
        # Crear productos
        self.crear_productos()
        
        self.stdout.write(self.style.SUCCESS('Datos iniciales creados exitosamente!'))

    def crear_usuarios(self):
        # Administrador
        if not Usuario.objects.filter(username='admin').exists():
            admin = Usuario.objects.create_user(
                username='admin',
                email='admin@splash.com',
                password='admin123',
                rol='administrador',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(f'✓ Administrador creado: {admin.username}')
        
        # Empleado
        if not Usuario.objects.filter(username='empleado').exists():
            empleado = Usuario.objects.create_user(
                username='empleado',
                email='empleado@splash.com',
                password='emp123',
                rol='empleado'
            )
            self.stdout.write(f'✓ Empleado creado: {empleado.username}')

    def crear_categorias(self):
        categorias_data = [
            {'nombre': 'Helados', 'descripcion': 'Helados de diferentes sabores y tamaños'},
            {'nombre': 'Frozen Yogurt', 'descripcion': 'Frozen yogurt saludable y delicioso'},
            {'nombre': 'Paletas', 'descripcion': 'Paletas heladas de agua y crema'},
            {'nombre': 'Malteadas', 'descripcion': 'Malteadas cremosas y refrescantes'},
            {'nombre': 'Bebidas', 'descripcion': 'Bebidas variadas y refrescos'},
        ]
        
        for cat_data in categorias_data:
            categoria, created = Categoria.objects.get_or_create(
                nombre=cat_data['nombre'],
                defaults={'descripcion': cat_data['descripcion']}
            )
            if created:
                self.stdout.write(f'✓ Categoría creada: {categoria.nombre}')

    def crear_productos(self):
        # Obtener categorías
        helados_cat = Categoria.objects.get(nombre='Helados')
        frozen_cat = Categoria.objects.get(nombre='Frozen Yogurt')
        paletas_cat = Categoria.objects.get(nombre='Paletas')
        malteadas_cat = Categoria.objects.get(nombre='Malteadas')
        bebidas_cat = Categoria.objects.get(nombre='Bebidas')
        
        productos_data = [
            # Helados
            {'nombre': 'Helado Chocolate Pequeño', 'tipo': 'helado', 'precio': 35.00, 'stock': 50, 'categoria': helados_cat},
            {'nombre': 'Helado Chocolate Mediano', 'tipo': 'helado', 'precio': 45.00, 'stock': 40, 'categoria': helados_cat},
            {'nombre': 'Helado Chocolate Grande', 'tipo': 'helado', 'precio': 60.00, 'stock': 30, 'categoria': helados_cat},
            {'nombre': 'Helado Vainilla Pequeño', 'tipo': 'helado', 'precio': 35.00, 'stock': 45, 'categoria': helados_cat},
            {'nombre': 'Helado Vainilla Mediano', 'tipo': 'helado', 'precio': 45.00, 'stock': 35, 'categoria': helados_cat},
            {'nombre': 'Helado Vainilla Grande', 'tipo': 'helado', 'precio': 60.00, 'stock': 25, 'categoria': helados_cat},
            {'nombre': 'Helado Fresa Pequeño', 'tipo': 'helado', 'precio': 35.00, 'stock': 40, 'categoria': helados_cat},
            {'nombre': 'Helado Fresa Mediano', 'tipo': 'helado', 'precio': 45.00, 'stock': 30, 'categoria': helados_cat},
            {'nombre': 'Helado Fresa Grande', 'tipo': 'helado', 'precio': 60.00, 'stock': 20, 'categoria': helados_cat},
            
            # Frozen Yogurt
            {'nombre': 'Frozen Yogurt Fresa Pequeño', 'tipo': 'frozen_yogurt', 'precio': 40.00, 'stock': 35, 'categoria': frozen_cat},
            {'nombre': 'Frozen Yogurt Fresa Mediano', 'tipo': 'frozen_yogurt', 'precio': 50.00, 'stock': 25, 'categoria': frozen_cat},
            {'nombre': 'Frozen Yogurt Fresa Grande', 'tipo': 'frozen_yogurt', 'precio': 65.00, 'stock': 15, 'categoria': frozen_cat},
            {'nombre': 'Frozen Yogurt Mango Pequeño', 'tipo': 'frozen_yogurt', 'precio': 40.00, 'stock': 30, 'categoria': frozen_cat},
            {'nombre': 'Frozen Yogurt Mango Mediano', 'tipo': 'frozen_yogurt', 'precio': 50.00, 'stock': 20, 'categoria': frozen_cat},
            {'nombre': 'Frozen Yogurt Mango Grande', 'tipo': 'frozen_yogurt', 'precio': 65.00, 'stock': 10, 'categoria': frozen_cat},
            
            # Paletas
            {'nombre': 'Paleta de Agua Fresa', 'tipo': 'paleta', 'precio': 20.00, 'stock': 90, 'categoria': paletas_cat},
            {'nombre': 'Paleta de Agua Limón', 'tipo': 'paleta', 'precio': 20.00, 'stock': 85, 'categoria': paletas_cat},
            {'nombre': 'Paleta de Agua Mango', 'tipo': 'paleta', 'precio': 20.00, 'stock': 80, 'categoria': paletas_cat},
            {'nombre': 'Paleta de Crema Chocolate', 'tipo': 'paleta', 'precio': 25.00, 'stock': 75, 'categoria': paletas_cat},
            {'nombre': 'Paleta de Crema Vainilla', 'tipo': 'paleta', 'precio': 25.00, 'stock': 70, 'categoria': paletas_cat},
            {'nombre': 'Paleta de Crema Fresa', 'tipo': 'paleta', 'precio': 25.00, 'stock': 65, 'categoria': paletas_cat},
            
            # Malteadas
            {'nombre': 'Malteada Chocolate Pequeña', 'tipo': 'malteada', 'precio': 45.00, 'stock': 40, 'categoria': malteadas_cat},
            {'nombre': 'Malteada Chocolate Mediana', 'tipo': 'malteada', 'precio': 55.00, 'stock': 35, 'categoria': malteadas_cat},
            {'nombre': 'Malteada Chocolate Grande', 'tipo': 'malteada', 'precio': 70.00, 'stock': 25, 'categoria': malteadas_cat},
            {'nombre': 'Malteada Vainilla Pequeña', 'tipo': 'malteada', 'precio': 45.00, 'stock': 35, 'categoria': malteadas_cat},
            {'nombre': 'Malteada Vainilla Mediana', 'tipo': 'malteada', 'precio': 55.00, 'stock': 30, 'categoria': malteadas_cat},
            {'nombre': 'Malteada Vainilla Grande', 'tipo': 'malteada', 'precio': 70.00, 'stock': 20, 'categoria': malteadas_cat},
            
            # Bebidas
            {'nombre': 'Agua Natural', 'tipo': 'bebida', 'precio': 15.00, 'stock': 100, 'categoria': bebidas_cat},
            {'nombre': 'Refresco Cola', 'tipo': 'bebida', 'precio': 20.00, 'stock': 95, 'categoria': bebidas_cat},
            {'nombre': 'Refresco Naranja', 'tipo': 'bebida', 'precio': 20.00, 'stock': 90, 'categoria': bebidas_cat},
            {'nombre': 'Jugo de Naranja', 'tipo': 'bebida', 'precio': 25.00, 'stock': 80, 'categoria': bebidas_cat},
            {'nombre': 'Jugo de Manzana', 'tipo': 'bebida', 'precio': 25.00, 'stock': 75, 'categoria': bebidas_cat},
        ]
        
        for prod_data in productos_data:
            producto, created = Producto.objects.get_or_create(
                nombre=prod_data['nombre'],
                defaults={
                    'tipo': prod_data['tipo'],
                    'precio': prod_data['precio'],
                    'stock': prod_data['stock'],
                    'categoria': prod_data['categoria'],
                    'activo': True
                }
            )
            if created:
                self.stdout.write(f'✓ Producto creado: {producto.nombre}')
            else:
                # Actualizar stock si ya existe
                producto.stock = prod_data['stock']
                producto.activo = True
                producto.save()
                self.stdout.write(f'↺ Producto actualizado: {producto.nombre}')
