# 🍦 SPLASH - Sistema POS para Heladería

Sistema completo de Punto de Venta (POS) diseñado específicamente para heladerías, enfocado en velocidad, simplicidad y facilidad de uso.

## 🎯 Características Principales

### POS (Punto de Venta)
- **Interfaz rápida y simple**: Botones grandes y claros para uso en caja
- **Carrito en tiempo real**: Actualización automática sin recargar página
- **Búsqueda instantánea**: Encuentra productos rápidamente
- **Control de stock**: Evita ventas sin inventario disponible
- **Tickets automáticos**: Generación de comprobantes detallados

### Gestión de Inventario
- **Control por producto**: Sin complicaciones de sabores
- **Stock automático**: Descuento automático al vender
- **Alertas de stock bajo**: Notificación visual para reabastecer
- **Categorías organizadas**: Agrupación lógica de productos

### Administración
- **Panel de control**: Estadísticas en tiempo real
- **Reportes de ventas**: Análisis por períodos
- **Productos más vendidos**: Identificación de favoritos
- **Roles de usuario**: Administrador y Empleado

## 🚀 Tecnologías

- **Backend**: Django 4.2.7
- **Base de datos**: PostgreSQL (obligatorio)
- **Frontend**: HTML5, CSS3, JavaScript vanilla
- **Diseño**: Responsive con colores corporativos

## 🎨 Colores Corporativos

- **Rojo**: `#FC182B`
- **Azul oscuro**: `#273D86`
- **Blanco**: `#FFFFFF`

## 📋 Requisitos

- Python 3.8+
- PostgreSQL 12+
- Navegador web moderno

## 🛠️ Instalación

### 1. Clonar el proyecto
```bash
git clone <repositorio>
cd splash_pos
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos
```bash
# Copiar archivo de configuración
cp .env.example .env

# Editar .env con tus datos de PostgreSQL
DATABASE_URL=postgresql://usuario:password@host:5432/splash_db?sslmode=require
```

### 5. Migrar base de datos
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario
```bash
python manage.py createsuperuser
```

### 7. Recolectar archivos estáticos
```bash
python manage.py collectstatic
```

### 8. Iniciar servidor
```bash
python manage.py runserver
```

## 👥 Usuarios y Roles

### Administrador
- Acceso completo al sistema
- Panel de administración
- Gestión de productos y categorías
- Reportes y estadísticas
- Acceso al POS

### Empleado
- Solo acceso al POS
- Procesamiento de ventas
- No puede ver reportes
- No puede modificar inventario

## 📦 Productos Predefinidos

El sistema maneja 5 tipos de productos:

1. **Helados** (pequeño, mediano, grande)
2. **Frozen Yogurt** (pequeño, mediano, grande)
3. **Paletas** (precio único)
4. **Malteadas** (pequeño, mediano, grande)
5. **Bebidas**

**Importante**: El inventario se maneja por producto, no por sabores.

## 🔧 Configuración Inicial

### 1. Acceder al panel de administración
```
http://localhost:8000/admin/
```

### 2. Crear categorías
- Helados
- Frozen Yogurt
- Paletas
- Malteadas
- Bebidas

### 3. Agregar productos
Ejemplos:
- Helado Chocolate - $45 - Stock: 50
- Helado Vainilla - $45 - Stock: 50
- Paleta Fresa - $25 - Stock: 90
- Malteada Grande - $60 - Stock: 30

### 4. Crear usuarios
- Administrador: acceso completo
- Empleado: solo POS

## 🌐 Despliegue en Render

### 1. Preparar para producción
```bash
# En .env
DEBUG=False
ALLOWED_HOSTS=tu-dominio.onrender.com
```

### 2. Archivo render.yaml (opcional)
```yaml
services:
  - type: web
    name: splash-pos
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn splash_pos.wsgi:application
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: splash-db
          property: connectionString
```

## 📱 Uso del POS

### 1. Iniciar sesión
- Usuario y contraseña configurados

### 2. Agregar productos
- Click en los botones de productos
- O usar la búsqueda

### 3. Gestionar carrito
- Ajustar cantidades con +/-
- Eliminar productos individualmente
- Vaciar carrito completo

### 4. Procesar venta
- Click en "PAGAR"
- Confirmar venta
- Ticket automático en nueva ventana

## 🧾 Tickets

El sistema genera tickets con:
- Número de ticket
- Fecha y hora
- Detalle de productos
- Total pagado
- Método de pago (efectivo)

## 📊 Reportes

### Dashboard Administrativo
- Ventas del día
- Ventas del mes
- Productos más vendidos
- Ventas recientes

### Reportes de Ventas
- Historial completo
- Filtrado por fechas
- Paginación
- Exportación de tickets

## 🔐 Seguridad

- Autenticación de usuarios
- Roles y permisos
- CSRF protection
- Validación de stock
- Sin pagos online (solo efectivo)

## 🐛 Troubleshooting

### Problemas comunes:

1. **Error de conexión PostgreSQL**
   - Verificar DATABASE_URL
   - Confirmar que PostgreSQL está corriendo
   - Revisar credenciales

2. **Error de archivos estáticos**
   - Ejecutar `python manage.py collectstatic`
   - Verificar configuración STATIC_URL

3. **Productos no aparecen**
   - Verificar que estén activos
   - Confirmar stock > 0
   - Revisar categorías

## 📞 Soporte

Para soporte técnico:
- Revisar logs del servidor
- Verificar configuración de base de datos
- Confirmar versión de Python y Django

## 📄 Licencia

Este proyecto es propiedad de SPLASH Heladería.
Uso exclusivo para operaciones internas.
