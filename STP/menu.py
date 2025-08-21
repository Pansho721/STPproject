from Clases import Plato

menu = {
    1: Plato(
        precio=7500,
        categoria="Pasta",
        nombre="Fideos a la Bolognesa",
        foto="fideos_bolognesa.jpg",
        ingredientes=["fideos", "carne molida", "salsa de tomate", "zanahoria", "cebolla"]
    ),
    2: Plato(
        precio=9500,
        categoria="Pasta",
        nombre="Lasagna",
        foto="lasagna.jpg",
        ingredientes=["masa", "queso", "salsa bechamel", "carne molida", "salsa de tomate"]
    ),
    3: Plato(
        precio=6000,
        categoria="Ensalada",
        nombre="Ensalada César",
        foto="ensalada_cesar.jpg",
        ingredientes=["lechuga", "pollo", "queso parmesano", "crutones", "salsa cesar"]
    ),
    4: Plato(
        precio=9300,
        categoria="Carnes",
        nombre="Pollo al horno con papas",
        foto="pollo_horno.jpg",
        ingredientes=["pollo", "papas", "ajo", "romero", "aceite de oliva"]
    ),
    5: Plato(
        precio=9800,
        categoria="Pasta",
        nombre="Ravioles de ricotta y espinaca",
        foto="ravioles.jpg",
        ingredientes=["ravioles", "ricotta", "espinaca", "salsa de tomate", "queso"]
    ),
}