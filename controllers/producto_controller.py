from decimal import Decimal, InvalidOperation
from models import producto_model

class ProductoController:
    def __init__(self, vista):
        self.vista = vista

    def cargar_productos(self):
        try:
            productos = producto_model.listar_productos()
            filas = [
                (
                    p[0],
                    p[1],
                    p[2],
                    f"{float(p[3]):.2f}",
                    "Disponible" if p[4] else "Agotado"
                )
                for p in productos
            ]
            self.vista.poblar_tabla(filas)
        except Exception as error:
            self.vista.mostrar_error(f"Error al listar productos: {error}")

    def abrir_modal_nuevo(self):
        self.vista.abrir_modal_registro(self.procesar_guardar_modal)

    def procesar_guardar_modal(self, datos, modal):
        nombre = datos.get("nombre", "").strip()
        categoria = datos.get("categoria", "").strip()
        precio_str = datos.get("precio", "").strip()
        disponible = datos.get("disponible", True)

        if not nombre or len(nombre) < 2:
            self.vista.mostrar_error("El nombre del plato debe tener al menos 2 caracteres.")
            return

        if not categoria:
            self.vista.mostrar_error("Debe seleccionar una categoría válida.")
            return

        try:
            precio_exacto = Decimal(precio_str)
            if precio_exacto <= Decimal('0.00'):
                self.vista.mostrar_error("El precio debe ser estrictamente mayor a 0.")
                return
        except (InvalidOperation, ValueError):
            self.vista.mostrar_error("El precio debe ser un número válido (ejemplo: 28.50).")
            return

        try:
            nuevo_id = producto_model.insertar_producto(nombre, categoria, precio_exacto, disponible)
            if nuevo_id:
                modal.destroy()  # Cierra la ventana emergente
                self.vista.mostrar_exito("Plato agregado a la carta exitosamente.")
                self.cargar_productos()  # Actualiza la tabla automáticamente
            else:
                self.vista.mostrar_error("No se pudo guardar el plato en la base de datos.")
        except Exception as error:
            self.vista.mostrar_error(f"Error al guardar plato: {error}")