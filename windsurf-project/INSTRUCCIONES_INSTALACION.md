# 🍦 SPLASH POS - Instrucciones de Instalación

## 📋 Resumen del Proyecto
Sistema de Punto de Venta (POS) para heladería con:
- **Panel de Administración** completo
- **Sistema de Ventas** intuitivo
- **Gestión de Productos** y Categorías
- **Control de Usuarios** y roles
- **Análisis de Ganancias** con exportación CSV

## 🚀 Pasos para Instalación en tu Laptop

### 1. **Requisitos Previos**
```bash
# Python 3.8+ (verificar versión)
python --version

# Pip (gestor de paquetes)
pip --version
```

### 2. **Descomprimir el Proyecto**
```bash
# Descomprimir el archivo .tar.gz
tar -xzf splash_pos_project.tar.gz

# Entrar al directorio del proyecto
cd windsurf-project
```

### 3. **Crear Entorno Virtual**
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate
```

### 4. **Instalar Dependencias**
```bash
# Instalar Django y paquetes necesarios
pip install django==4.2
pip install psycopg2-binary
pip install python-decouple
```

### 5. **Configurar Base de Datos**
```bash
# Realizar migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario (administrador)
python manage.py createsuperuser
```

### 6. **Cargar Datos Iniciales**
```bash
# Opcional: Cargar productos de ejemplo
python manage.py shell
# Luego ejecutar el script que está en README.md
```

### 7. **Iniciar el Servidor**
```bash
# Iniciar servidor de desarrollo
python manage.py runserver

# Acceder a la aplicación
# URL: http://127.0.0.1:8000
```

## 👤 **Usuarios de Acceso**

### **Administrador Principal**
- **Usuario:** admin
- **Contraseña:** admin123
- **Rol:** Administrador

### **Cajero de Ejemplo**
- **Usuario:** cajero
- **Contraseña:** cajero123
- **Rol:** Cajero

## 🎯 **URLs Importantes**

### **Acceso Principal**
- **Login:** http://127.0.0.1:8000/
- **Panel POS:** http://127.0.0.1:8000/pos/
- **Admin Dashboard:** http://127.0.0.1:8000/admin/dashboard/

### **Secciones de Administración**
- **Ventas:** http://127.0.0.1:8000/admin/ventas/
- **Productos:** http://127.0.0.1:8000/admin/productos/
- **Configuración:** http://127.0.0.1:8000/admin/config/
- **Ganancias:** http://127.0.0.1:8000/admin/ganancias/

## 🔧 **Configuración Adicional**

### **Base de Datos PostgreSQL (Opcional)**
```python
# En settings.py, cambiar:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'splash_pos',
        'USER': 'postgres',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### **Producción**
```bash
# Instalar dependencias adicionales
pip install gunicorn
pip install whitenoise

# Recolectar archivos estáticos
python manage.py collectstatic

# Iniciar con Gunicorn
gunicorn splash_pos.wsgi:application
```

## 📁 **Estructura del Proyecto**
```
windsurf-project/
├── manage.py                 # Archivo principal de Django
├── requirements.txt          # Dependencias
├── README.md                # Documentación completa
├── splash_pos/              # Configuración principal
│   ├── settings.py          # Configuración del proyecto
│   ├── urls.py             # URLs principales
│   └── wsgi.py             # Configuración WSGI
├── pos/                    # Aplicación principal
│   ├── models.py           # Modelos de datos
│   ├── views.py            # Lógica de la aplicación
│   ├── forms.py            # Formularios
│   ├── urls.py             # URLs de la app
│   ├── admin.py            # Panel Django Admin
│   └── templates/pos/      # Plantillas HTML
└── static/                 # Archivos estáticos
    ├── css/               # Estilos CSS
    ├── js/                # JavaScript
    └── images/            # Imágenes
```

## 🎨 **Características Implementadas**

### **✅ Panel de Administración**
- Dashboard con estadísticas en tiempo real
- Gestión completa de productos y categorías
- Control de usuarios y permisos
- Historial detallado de ventas
- Análisis de ganancias con exportación CSV

### **✅ Sistema de Ventas**
- Interfaz intuitiva de punto de venta
- Selección rápida de productos
- Gestión de carrito en tiempo real
- Generación automática de tickets
- Procesamiento de pagos

### **✅ Diseño y UX**
- Interfaz moderna y responsive
- Colores corporativos consistentes
- Tipografía optimizada para legibilidad
- Animaciones y transiciones suaves
- Accesibilidad WCAG

## 🆘 **Soporte y Solución de Problemas**

### **Problemas Comunes**
1. **Error de migración:** Ejecutar `python manage.py makemigrations pos`
2. **Error de permisos:** Verificar configuración de archivos estáticos
3. **Error de base de datos:** Revisar configuración en settings.py
4. **Error de importación:** Activar entorno virtual correctamente

### **Comandos Útiles**
```bash
# Verificar instalación
python manage.py check

# Crear superusuario adicional
python manage.py createsuperuser

# Ver migraciones aplicadas
python manage.py showmigrations

# Reiniciar servidor
python manage.py runserver
```

## 📞 **Contacto de Soporte**
Si tienes problemas durante la instalación, revisa:
1. El archivo README.md completo
2. La documentación de Django
3. Los logs de error del servidor

---

**¡Listo para usar!** 🎉
El sistema SPLASH POS está completamente funcional y listo para operar tu heladería.
