# Importaciones necesarias de Django y otras utilidades
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import models
from collections import Counter

# Importación de modelos y formularios propios de la aplicación
from comidapp.models import Pedido, Cliente, Plato, Admin, Comentario
from .forms import NuevoPlato, ModificarPlato, ComentarioForm

# Vista principal que responde solo a solicitudes GET y carga la página principal
def main_view(request):
    if request.method == "GET":
        return render(request, "comidapp/main.html")

# Función auxiliar que toma un carrito (diccionario de id de platos y cantidades)
# y retorna el contenido detallado del pedido, precio total y cantidad total
def getPedidoFromCart(cart):
    pedido = []
    total_precio = 0
    total_items = 0
    for plato_id, cantidad in cart.items():
        try:
            plato = Plato.objects.get(id=plato_id)  # Buscar plato por id
            plato.cantidad = cantidad
            pedido.append(plato)
            total_precio += plato.precio * cantidad
            total_items += cantidad
        except Plato.DoesNotExist:
            continue  # Ignora si el plato no existe
    return cart, pedido, total_precio, total_items

# Vista para mostrar el menú al cliente y gestionar el carrito de pedidos
def cliente_view(request):
    menu = Plato.objects.all()  # Obtener todos los platos
    cart = request.session.get('cart', {})  # Obtener carrito desde la sesión

    # Calcular el promedio de puntuación y agregar comentarios a cada plato
    for plato in menu:
        comentarios = Comentario.objects.filter(plato=plato)
        if comentarios.exists():
            promedio = comentarios.aggregate(models.Avg('puntuacion'))['puntuacion__avg']
            plato.promedio_puntuacion = round(promedio, 1)
        else:
            plato.promedio_puntuacion = None
        plato.comentarios.set(comentarios)

    if request.method == "GET":
        # Mostrar menú y contenido del carrito
        cart, pedido, total_precio, total_items = getPedidoFromCart(cart)  
        return render(request, "comidapp/menu.html", {'menu': menu,
                                                      'pedido': pedido,
                                                      'total_precio': total_precio,
                                                      'total_items': total_items})
    if request.method == "POST":
        # Añadir o modificar cantidad de un plato en el carrito
        plato_id = request.POST.get('plato_id')
        cantidad = int(request.POST.get('cantidad', 1))
        if plato_id in cart:
            cart[plato_id] += cantidad
        else:
            cart[plato_id] = cantidad
        request.session['cart'] = cart  # Guardar cambios en sesión

    # Actualizar carrito después de modificación
    cart, pedido, total_precio, total_items = getPedidoFromCart(cart)  
    return render(request, "comidapp/menu.html", {
        'menu': menu,
        'pedido': pedido,
        'total_precio': total_precio,
        'total_items': total_items
    })

# Limpia el carrito en la sesión y redirige al menú del cliente
def clear_cart(request):
    request.session['cart'] = {}
    return redirect('cliente_view')
    
# Vista que confirma el pedido y lo guarda en la base de datos
def confirmar_pedido(request):
    if request.method == 'POST':
        mesa = int(request.POST.get('mesa'))
        cart = request.session.get('cart', {})

        if not cart:
            return redirect('cliente_view')

        # Crear nuevo pedido con la mesa indicada y fecha actual
        nuevo_pedido = Pedido.objects.create(
            numero_mesa=mesa,
            fecha_creacion=timezone.now()
        )

        # Guardar información del último pedido en la sesión
        request.session['ultimo_pedido_id'] = nuevo_pedido.id
        request.session['ultimo_pedido_cart'] = cart.copy()

        # Añadir platos al pedido según su cantidad
        for plato_id, cantidad in cart.items():
            try:
                plato = Plato.objects.get(id=plato_id)
                for _ in range(cantidad):
                    nuevo_pedido.platos.add(plato)
            except Plato.DoesNotExist:
                continue

        # Limpiar carrito
        request.session['cart'] = {}

        return redirect('client_order')

# Vista de login previa a mostrar la interfaz de administración
def admin_preview(request):
    if request.method == "GET":
        return render(request, "comidapp/admin_preview.html")

    if request.method == "POST":
        if request.user.is_authenticated:
            return redirect('admin_preview')
        
        # Obtener credenciales
        username = request.POST.get("nombre")
        password = request.POST.get("contraseña")

        # Verificar autenticación
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_view')
        else:
            return render(request, "comidapp/admin_preview.html", {"error": "Credenciales inválidas"})

# Vista principal de administración donde se listan los nombres de los platos
def admin_view(request):
    nombres = Plato.objects.values_list('name', flat=True)

    if request.method == "GET":
        return render(request, "comidapp/admin_view.html", {"nombres": nombres})

# Vista para agregar un nuevo plato usando un formulario
def admin_add_view(request):
    if request.method == "POST": 
        form = NuevoPlato(request.POST)  
        if form.is_valid():
            form.save()
            form = NuevoPlato()  # Resetear formulario
    else:
        form = NuevoPlato()
    return render(request, 'comidapp/admin_add.html', {'form': form})

# Vista para mostrar el menú desde el punto de vista del administrador o cliente
def admin_menu_view(request):
    menu = Plato.objects.all()
    
    if request.method == "GET":
        if request.user.is_authenticated:
            return render(request, "comidapp/admin_menu.html", {'menu': menu})
        else:
            return render(request, "comidapp/menu.html", {'menu': menu})

# Vista para modificar los platos desde la administración
def admin_modify_menu(request):
    menu = Plato.objects.all()
    
    if request.method == "GET":
        return render(request, "comidapp/admin_modify.html", {'menu': menu})

# Vista para editar un plato específico
def admin_modify_dish(request, plato_id):
    plato = get_object_or_404(Plato, id=plato_id)

    if request.method == 'POST':
        form = ModificarPlato(request.POST, instance=plato)
        if form.is_valid():
            form.save()
            return redirect('admin_modify')
    else:
        form = ModificarPlato(instance=plato)

    return render(request, 'comidapp/dish_modify.html', {'form': form})

# Vista para eliminar un plato específico
def eliminar_plato(request, plato_id):
    plato = get_object_or_404(Plato, id=plato_id)
    if request.method == 'POST':
        plato.delete()
    return redirect('admin_modify')

# Vista para cerrar sesión del administrador
def logout_view(request):
    logout(request)
    return redirect('admin_preview')

# Vista que muestra los datos de contacto del equipo desarrollador
def contactos_view(request):
    contactos = [
        {"nombre": "Hugo González", "telegram": "@huwux"},
        {"nombre": "Gaspar Robledo", "telegram": "@robledooo"},
        {"nombre": "Juan Pablo Sánchez", "telegram": "@Aegfke"},
        {"nombre": "Gabriel Tapia", "telegram": "@angelesdepapel"},
        {"nombre": "Francisco Romero", "telegram": "@Pansho721"},
        {"nombre": "Jorge Contreras", "telegram": "@jr_gee"}
    ]
    return render(request, 'comidapp/contactos.html', {'contactos': contactos})

# Vista final que muestra el resumen del pedido y permite dejar comentarios
def final_view(request):
    pedido_id_mostrado = request.session.get('ultimo_pedido_id')
    if not pedido_id_mostrado:
        return render(request, 'comidapp/client_order.html', {'error': 'No se encontró ningún pedido.'})

    pedido = get_object_or_404(Pedido, id=pedido_id_mostrado)
    cart = request.session.get('ultimo_pedido_cart', {})
    
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            plato_id = request.POST.get('plato_id')
            plato = get_object_or_404(Plato, id=plato_id)
            nuevo_comentario = form.save(commit=False)
            nuevo_comentario.plato = plato 
            nuevo_comentario.save() 
            return redirect('client_order') 
    
    form = ComentarioForm()

    # Armar lista de platos con cantidad y precio total
    platos_con_cantidad = []
    for plato_id, cantidad in cart.items():
        try:
            plato = Plato.objects.get(id=plato_id)
            platos_con_cantidad.append({
                'plato': plato,
                'cantidad': cantidad,
                'precio_total': cantidad * plato.precio
            })
        except Plato.DoesNotExist:
            continue

    # Calcular total del pedido
    total_pedido = sum(item['precio_total'] for item in platos_con_cantidad)

    context = {
        'pedido': pedido,
        'platos_con_cantidad': platos_con_cantidad,
        'form': form,
        'total_pedido': total_pedido,
    }
    return render(request, 'comidapp/client_order.html', context)