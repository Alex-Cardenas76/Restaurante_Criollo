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

    def conmutar_disponibilidad(self):
        valores = self.vista.get_producto_seleccionado()
        if not valores:
            self.vista.mostrar_error("Por favor, seleccione un plato de la tabla para cambiar su estado.")
            return

        producto_id = int(valores[0])
        nombre_plato = valores[1]
        estado_actual = valores[4]  # "Disponible" o "Agotado"

        nueva_disponibilidad = (estado_actual != "Disponible")
        nuevo_texto = "Disponible" if nueva_disponibilidad else "Agotado"

        try:
            exito = producto_model.actualizar_disponibilidad(producto_id, nueva_disponibilidad)
            if exito:
                self.cargar_productos()
                self.vista.mostrar_exito(f"El plato '{nombre_plato}' ahora está marcado como '{nuevo_texto}'.")
            else:
                self.vista.mostrar_error("No se pudo actualizar el estado del plato.")
        except Exception as error:
            self.vista.mostrar_error(f"Error al cambiar disponibilidad: {error}")

    def abrir_modal_editar(self):
        valores = self.vista.get_producto_seleccionado()
        if not valores:
            self.vista.mostrar_error("Por favor, seleccione un plato de la tabla para editar.")
            return

        producto_id = int(valores[0])
        producto_datos = {
            "id": producto_id,
            "nombre": valores[1],
            "categoria": valores[2],
            "precio": valores[3],
            "disponible": valores[4] == "Disponible"
        }
        self.vista.abrir_modal_edicion(producto_datos, self.procesar_editar_modal)

    def procesar_editar_modal(self, datos, modal):
        producto_id = datos.get("id")
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
            exito = producto_model.actualizar_producto(
                producto_id=producto_id,
                nombre=nombre,
                categoria=categoria,
                precio=precio_exacto,
                disponible=disponible
            )
            if exito:
                modal.destroy()
                self.vista.mostrar_exito(f"Plato '{nombre}' actualizado exitosamente.")
                self.cargar_productos()
            else:
                self.vista.mostrar_error("No se realizaron cambios en el plato.")
        except Exception as error:
            self.vista.mostrar_error(f"Error al actualizar plato: {error}")

    def eliminar_producto_seleccionado(self):
        valores = self.vista.get_producto_seleccionado()
        if not valores:
            self.vista.mostrar_error("Por favor, seleccione un plato de la tabla para eliminar.")
            return

        producto_id = int(valores[0])
        nombre_plato = valores[1]

        # Verificar si tiene pedidos asociados para proteger la integridad contable
        try:
            if producto_model.producto_tiene_pedidos(producto_id):
                self.vista.mostrar_error(
                    f"⚠️ No se puede eliminar el plato '{nombre_plato}' porque ya cuenta con ventas y comandas asociadas en el historial contable.\n\n"
                    "Para sacarlo de la carta sin romper los registros contables, utilice el botón '🔄 Disponibilidad' y márquelo como 'Agotado'."
                )
                return

            confirmacion = self.vista.confirmar_accion(
                "Confirmar Eliminación",
                f"¿Está seguro de que desea eliminar definitivamente el plato '{nombre_plato}' de la carta?\n\nEsta acción no se puede deshacer."
            )
            if not confirmacion:
                return

            exito = producto_model.eliminar_producto(producto_id)
            if exito:
                self.cargar_productos()
                self.vista.mostrar_exito(f"El plato '{nombre_plato}' ha sido eliminado de la carta.")
            else:
                self.vista.mostrar_error("No se pudo eliminar el plato.")
        except Exception as error:
            self.vista.mostrar_error(f"Error al eliminar plato: {error}")