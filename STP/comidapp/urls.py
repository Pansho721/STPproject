from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name = 'main_view'),
    path('cliente/', views.cliente_view, name = 'cliente_view'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('confirmar_pedido/', views.confirmar_pedido, name='confirm_pedido'),
    path('admin_view/', views.admin_view, name = 'admin_view'),
    path('admin_preview/', views.admin_preview, name = 'admin_preview'),
    path('admin_addPlato/', views.admin_add_view, name='admin_add'),
    path('admin_menu/', views.admin_menu_view, name = 'admin_menu'),
    path('admin_modify/', views.admin_modify_menu, name = 'admin_modify'),
    path('dish_modify/<int:plato_id>/', views.admin_modify_dish, name = 'dish_modify'),
    path('plato/eliminar/<int:plato_id>/', views.eliminar_plato, name ='eliminar_plato'),
    path('logout/', views.logout_view, name='logout_view'),
    path('pedido_confirmado/', views.final_view, name = 'client_order'),
    path('contactos/', views.contactos_view, name = 'contactos_view'),
    
    # ahora mismo, admin-view y admin-NewPlato es la misma vista,
    # en un futuro, admin-view será el intermedio entre admin preview y el resto de
    # funcionalidades (modificar, eliminar, etc)
    #path('admin-view/', views.admin_view, name = 'admin_view'),
]  