from django import forms
from .models import Plato, Admin, Comentario

class NuevoPlato(forms.ModelForm):
    name = forms.CharField(
        label='Nombre del plato',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'inputName',
            'placeholder': 'Nombre del plato'
        })
    )
    list_ingredientes = forms.CharField(
        label='Lista de Ingredientes',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'inputIngredientes',
            'placeholder': 'Ejemplo: Tomate, Lechuga, Queso'
        })
    )
    categoria = forms.CharField(
        label='Categoría',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'inputCategoria',
            'placeholder': 'PlatoFondo, Entrada, o Bebestible'
        })
    )
    precio = forms.DecimalField(
        label='Precio',
        max_digits=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'inputPrecio',
            'placeholder': 'Ejemplo: 2500'
        })
    )

    class Meta:
        model = Plato
        fields = ['name', 'list_ingredientes', 'categoria', 'precio']

class IngresoAdmin(forms.ModelForm):
    name = forms.CharField(
        label='Nombre de usuario',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'inputUsername',
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'inputPassword',
        })
    )

    class Meta:
        model = Admin
        fields = ['name', 'password']

class ModificarPlato(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Ejemplo solo para el campo name
            self.fields['name'].widget.attrs.update({
                'placeholder': self.instance.name,
                'class': 'form-control',
                'id': 'inputName',
            })

    class Meta:
        model = Plato
        fields = ['name', 'list_ingredientes', 'categoria', 'precio']
        labels = {
            'name': 'Nombre',
            'list_ingredientes': 'Lista de ingredientes',
            'categoria': 'Categoría',
            'precio': 'Precio',
        }

class ComentarioForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['texto'].required = False
        
    class Meta:
        model = Comentario
        fields = ['texto', 'puntuacion'] # Campos que el usuario llenará
        widgets = {
            'texto': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-white', 
                'rows': 3,
                'placeholder': 'Escribe tu opinión aquí...'
            }),
            'puntuacion': forms.Select(attrs={
                'class': 'form-select bg-dark text-white'
            }),
        }
        labels = {
            'texto': 'Tu opinión',
            'puntuacion': 'Puntuación'
        }