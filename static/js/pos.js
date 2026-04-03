// Carrito y funcionalidad POS
class CarritoPOS {
    constructor() {
        this.carrito = [];
        this.init();
    }

    init() {
        this.cargarCarrito();
        this.setupEventListeners();
        this.setupSearch();
    }

    setupEventListeners() {
        // Event delegation para productos
        document.addEventListener('click', (e) => {
            if (e.target.closest('.producto-card') && !e.target.closest('.producto-card').classList.contains('agotado')) {
                const productoCard = e.target.closest('.producto-card');
                const productoId = productoCard.dataset.productoId;
                this.agregarAlCarrito(productoId, 1);
            }
        });

        // Botones de cantidad en el carrito
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('btn-cantidad-mas')) {
                const productoId = e.target.dataset.productoId;
                this.cambiarCantidad(productoId, 1);
            } else if (e.target.classList.contains('btn-cantidad-menos')) {
                const productoId = e.target.dataset.productoId;
                this.cambiarCantidad(productoId, -1);
            } else if (e.target.classList.contains('btn-eliminar')) {
                const productoId = e.target.dataset.productoId;
                this.eliminarDelCarrito(productoId);
            }
        });

        // Botones de acciones
        document.getElementById('btn-vaciar')?.addEventListener('click', () => this.vaciarCarrito());
        document.getElementById('btn-pagar')?.addEventListener('click', () => this.procesarVenta());
    }

    setupSearch() {
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            let searchTimeout;
            searchInput.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    this.buscarProductos(e.target.value);
                }, 300);
            });
        }
    }

    async agregarAlCarrito(productoId, cantidad = 1) {
        try {
            this.showLoading();
            const response = await fetch('/pos/agregar-al-carrito/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: JSON.stringify({ producto_id: productoId, cantidad }),
            });

            const data = await response.json();
            
            if (data.success) {
                this.carrito = data.carrito;
                this.actualizarCarritoUI();
                this.mostrarMensaje(data.message, 'success');
            } else {
                this.mostrarMensaje(data.error, 'error');
            }
        } catch (error) {
            this.mostrarMensaje('Error al agregar al carrito', 'error');
        } finally {
            this.hideLoading();
        }
    }

    async cambiarCantidad(productoId, cambio) {
        const item = this.carrito.find(item => item.producto_id == productoId);
        if (!item) return;

        const nuevaCantidad = item.cantidad + cambio;
        if (nuevaCantidad <= 0) {
            this.eliminarDelCarrito(productoId);
            return;
        }

        try {
            this.showLoading();
            const response = await fetch('/pos/actualizar-carrito/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: JSON.stringify({ producto_id: productoId, cantidad: nuevaCantidad }),
            });

            const data = await response.json();
            
            if (data.success) {
                this.carrito = data.carrito;
                this.actualizarCarritoUI();
            } else {
                this.mostrarMensaje(data.error, 'error');
            }
        } catch (error) {
            this.mostrarMensaje('Error al actualizar carrito', 'error');
        } finally {
            this.hideLoading();
        }
    }

    async eliminarDelCarrito(productoId) {
        try {
            this.showLoading();
            const response = await fetch('/pos/actualizar-carrito/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: JSON.stringify({ producto_id: productoId, cantidad: 0 }),
            });

            const data = await response.json();
            
            if (data.success) {
                this.carrito = data.carrito;
                this.actualizarCarritoUI();
            } else {
                this.mostrarMensaje(data.error, 'error');
            }
        } catch (error) {
            this.mostrarMensaje('Error al eliminar del carrito', 'error');
        } finally {
            this.hideLoading();
        }
    }

    async vaciarCarrito() {
        if (!confirm('¿Estás seguro de vaciar el carrito?')) return;

        try {
            this.showLoading();
            const response = await fetch('/pos/vaciar-carrito/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
            });

            const data = await response.json();
            
            if (data.success) {
                this.carrito = data.carrito;
                this.actualizarCarritoUI();
                this.mostrarMensaje('Carrito vaciado', 'success');
            } else {
                this.mostrarMensaje(data.error, 'error');
            }
        } catch (error) {
            this.mostrarMensaje('Error al vaciar carrito', 'error');
        } finally {
            this.hideLoading();
        }
    }

    async procesarVenta() {
        if (this.carrito.length === 0) {
            this.mostrarMensaje('El carrito está vacío', 'error');
            return;
        }

        if (!confirm('¿Confirmar venta?')) return;

        try {
            this.showLoading();
            const response = await fetch('/pos/procesar-venta/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
            });

            const data = await response.json();
            
            if (data.success) {
                this.carrito = [];
                this.actualizarCarritoUI();
                this.mostrarMensaje(data.message, 'success');
                
                // Abrir ticket en nueva ventana
                window.open(`/pos/ticket/${data.venta_id}/`, '_blank');
                
                // Actualizar productos
                this.actualizarProductos();
            } else {
                this.mostrarMensaje(data.error, 'error');
            }
        } catch (error) {
            this.mostrarMensaje('Error al procesar venta', 'error');
        } finally {
            this.hideLoading();
        }
    }

    async buscarProductos(query) {
        if (query.length < 2) {
            this.mostrarTodosLosProductos();
            return;
        }

        try {
            const response = await fetch(`/pos/buscar-productos/?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            this.filtrarProductos(data.productos);
        } catch (error) {
            console.error('Error al buscar productos:', error);
        }
    }

    actualizarCarritoUI() {
        // Actualizar items del carrito
        const carritoItems = document.getElementById('carrito-items');
        if (carritoItems) {
            if (this.carrito.length === 0) {
                carritoItems.innerHTML = '<p class="text-center text-muted">El carrito está vacío</p>';
            } else {
                carritoItems.innerHTML = this.carrito.map(item => `
                    <div class="carrito-item slide-in">
                        <div class="carrito-item-info">
                            <div class="carrito-item-nombre">${item.nombre}</div>
                            <div class="carrito-item-precio">$${item.precio.toFixed(2)} c/u</div>
                        </div>
                        <div class="carrito-item-cantidad">
                            <button class="btn-cantidad btn-cantidad-menos" data-producto-id="${item.producto_id}">-</button>
                            <span>${item.cantidad}</span>
                            <button class="btn-cantidad btn-cantidad-mas" data-producto-id="${item.producto_id}">+</button>
                            <button class="btn-eliminar" data-producto-id="${item.producto_id}">Eliminar</button>
                        </div>
                    </div>
                `).join('');
            }
        }

        // Actualizar resumen
        const total = this.carrito.reduce((sum, item) => sum + item.subtotal, 0);
        const totalItems = this.carrito.reduce((sum, item) => sum + item.cantidad, 0);

        const subtotalElement = document.getElementById('subtotal');
        const totalElement = document.getElementById('total');
        const totalItemsElement = document.getElementById('total-items');

        if (subtotalElement) subtotalElement.textContent = `$${total.toFixed(2)}`;
        if (totalElement) totalElement.textContent = `$${total.toFixed(2)}`;
        if (totalItemsElement) totalItemsElement.textContent = totalItems;

        // Habilitar/deshabilitar botón de pago
        const btnPagar = document.getElementById('btn-pagar');
        if (btnPagar) {
            btnPagar.disabled = this.carrito.length === 0;
        }

        // Guardar en sesión
        this.guardarCarrito();
    }

    filtrarProductos(productos) {
        const allCards = document.querySelectorAll('.producto-card');
        const productosIds = productos.map(p => p.id.toString());

        allCards.forEach(card => {
            const productoId = card.dataset.productoId;
            if (productosIds.includes(productoId)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }

    mostrarTodosLosProductos() {
        const allCards = document.querySelectorAll('.producto-card');
        allCards.forEach(card => {
            card.style.display = 'block';
        });
    }

    actualizarProductos() {
        // Recargar la página para actualizar el stock
        setTimeout(() => {
            window.location.reload();
        }, 1000);
    }

    mostrarMensaje(mensaje, tipo = 'info') {
        // Crear elemento de mensaje
        const mensajeDiv = document.createElement('div');
        mensajeDiv.className = `alert alert-${tipo === 'error' ? 'danger' : tipo} fade-in`;
        mensajeDiv.textContent = mensaje;
        mensajeDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        `;

        if (tipo === 'success') {
            mensajeDiv.style.backgroundColor = '#d4edda';
            mensajeDiv.style.color = '#155724';
            mensajeDiv.style.border = '1px solid #c3e6cb';
        } else if (tipo === 'error') {
            mensajeDiv.style.backgroundColor = '#f8d7da';
            mensajeDiv.style.color = '#721c24';
            mensajeDiv.style.border = '1px solid #f5c6cb';
        }

        document.body.appendChild(mensajeDiv);

        // Eliminar después de 3 segundos
        setTimeout(() => {
            mensajeDiv.remove();
        }, 3000);
    }

    showLoading() {
        const btnPagar = document.getElementById('btn-pagar');
        if (btnPagar) {
            btnPagar.disabled = true;
            btnPagar.innerHTML = '<span class="loading"></span> Procesando...';
        }
    }

    hideLoading() {
        const btnPagar = document.getElementById('btn-pagar');
        if (btnPagar) {
            btnPagar.disabled = this.carrito.length === 0;
            btnPagar.innerHTML = 'PAGAR';
        }
    }

    getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return decodeURIComponent(value);
            }
        }
        return '';
    }

    guardarCarrito() {
        // El carrito se guarda automáticamente en la sesión del servidor
    }

    cargarCarrito() {
        // El carrito se carga automáticamente del servidor al cargar la página
        this.actualizarCarritoUI();
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new CarritoPOS();
});

// Funciones globales
function formatCurrency(amount) {
    return new Intl.NumberFormat('es-MX', {
        style: 'currency',
        currency: 'MXN'
    }).format(amount);
}

function printTicket() {
    window.print();
}

// Atajos de teclado
document.addEventListener('keydown', (e) => {
    // Ctrl+P para imprimir ticket
    if (e.ctrlKey && e.key === 'p') {
        e.preventDefault();
        printTicket();
    }
    
    // Escape para limpiar búsqueda
    if (e.key === 'Escape') {
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            searchInput.value = '';
            searchInput.dispatchEvent(new Event('input'));
        }
    }
});
