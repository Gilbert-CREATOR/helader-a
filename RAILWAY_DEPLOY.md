# 🚀 Deploy de SPLASH POS en Railway

## 📋 Pasos para Deploy en Railway

### 1. **Preparar el Repositorio**
```bash
# Asegurarse que todo está en GitHub
git add .
git commit -m "🚀 Ready for Railway deploy"
git push origin main
```

### 2. **Configurar Railway**
1. **Ir a:** https://railway.app/
2. **Login** con GitHub
3. **New Project** → **Deploy from GitHub repo**
4. **Seleccionar:** `Gilbert-CREATOR/helader-a`
5. **Branch:** `main`

### 3. **Configurar Variables de Entorno**
En Railway Dashboard → Variables:

#### **Variables Requeridas:**
```
DJANGO_SETTINGS_MODULE=splash_pos.settings
SECRET_KEY=django-insecure-genera-una-clave-secreta-unica
DEBUG=False
ALLOWED_HOSTS=.railway.app,localhost,127.0.0.1
```

#### **Base de Datos (Railway la provee):**
```
DATABASE_URL=postgresql://postgres:password@containers-us-west-xxx.railway.app:5432/railway
```
*(Railway asignará automáticamente esta variable)*

### 4. **Configurar Build Settings**
En Railway Dashboard → Settings:

#### **Build Command:**
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

#### **Start Command:**
```bash
gunicorn splash_pos.wsgi:application --bind 0.0.0.0:$PORT
```

#### **Python Version:**
```
python-3.9.16
```

### 5. **Archivos de Configuración**
El proyecto ya incluye:

#### **Procfile:**
```
web: gunicorn splash_pos.wsgi:application --bind 0.0.0.0:$PORT
```

#### **runtime.txt:**
```
python-3.9.16
```

#### **railway.toml:**
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "gunicorn splash_pos.wsgi:application --bind 0.0.0.0:$PORT"
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 10

[env]
DJANGO_SETTINGS_MODULE = "splash_pos.settings"
PYTHONPATH = "/app"
```

### 6. **Deploy Automático**
1. **Push a GitHub** → Railway detecta cambios
2. **Build automático** → Instala dependencias
3. **Deploy** → Aplicación en línea

### 7. **Migraciones Iniciales**
Después del primer deploy, ejecutar migraciones:

#### **Opción A: Railway Console**
1. **Railway Dashboard** → Project
2. **Console** → New Console
3. **Comando:**
```bash
python manage.py migrate
python manage.py createsuperuser
```

#### **Opción B: Agregar a Build**
Actualizar build command:
```bash
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
```

### 8. **URL del Deploy**
Railway asignará una URL como:
```
https://splash-pos-production.up.railway.app
```

## 🔧 **Configuración Adicional**

### **Archivos Estáticos**
```python
# settings.py ya configurado
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

### **Seguridad**
```python
# settings.py ya configurado para producción
DEBUG = False
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

### **Base de Datos**
```python
# settings.py detecta automáticamente DATABASE_URL
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(default=config('DATABASE_URL'))
    }
```

## 🎯 **Verificación del Deploy**

### **1. Verificar Logs**
- Railway Dashboard → Logs
- Buscar errores de migración o configuración

### **2. Verificar URL**
Acceder a la URL asignada y verificar:
- ✅ Carga la página de login
- ✅ Los archivos estáticos cargan
- ✅ No hay errores 500

### **3. Crear Admin**
Si no se creó automáticamente:
```bash
# En Railway Console
python manage.py createsuperuser
```

## 🚨 **Problemas Comunes y Soluciones**

### **Error 500 - DEBUG=False**
```python
# Asegurar que ALLOWED_HOSTS incluya el dominio
ALLOWED_HOSTS = ['.railway.app', 'localhost', '127.0.0.1']
```

### **Archivos Estáticos no cargan**
```bash
# En build command o console
python manage.py collectstatic --noinput --clear
```

### **Error de Base de Datos**
```bash
# Verificar DATABASE_URL en variables de entorno
python manage.py migrate --run-syncdb
```

### **Error de Migraciones**
```bash
# Resetear migraciones
python manage.py migrate --fake-initial
```

## 🎉 **Resultado Final**

### **URL Pública:**
```
https://tu-splash-pos.up.railway.app
```

### **Usuarios de Acceso:**
- **Admin:** Crear durante deploy
- **Cajero:** Crear desde panel admin

### **Funcionalidades Completas:**
- ✅ Panel de administración
- ✅ Sistema de ventas POS
- ✅ Gestión de productos
- ✅ Análisis de ganancias
- ✅ Exportación CSV

---

**¡Listo para producción en Railway!** 🚀✨
