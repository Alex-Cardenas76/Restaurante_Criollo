import re
from models import cliente_model

class ClienteController:
    def __init__(self, vista):
        self.vista = vista

    def cargar_clientes(self):
        try:
            clientes = cliente_model.listar_clientes()
            # Formatear: (id, dni, nombre, telefono)
            filas = [(c[0], c[2], c[1], c[3] or "-") for c in clientes]
            self.vista.poblar_tabla(filas)
        except Exception as error:
            self.vista.mostrar_error(f"Error al listar clientes: {error}")

    def abrir_modal_nuevo(self):
        self.vista.abrir_modal_registro(self.procesar_guardar_modal)

    def procesar_guardar_modal(self, datos, modal):
        dni = datos.get("dni", "").strip()
        nombres = datos.get("nombres", "").strip()
        telefono = datos.get("telefono", "").strip()

        # Validaciones de reglas de negocio
        if not re.fullmatch(r'\d{8}', dni):
            self.vista.mostrar_error("El DNI debe tener exactamente 8 dígitos numéricos.")
            return

        if len(nombres) < 3 or not re.fullmatch(r'[A-Za-zÁ-Úá-úÑñ\s]+', nombres):
            self.vista.mostrar_error("El nombre debe tener al menos 3 caracteres y solo contener letras.")
            return

        if telefono and not re.fullmatch(r'9\d{8}', telefono):
            self.vista.mostrar_error("El teléfono debe ser un celular válido de 9 dígitos que inicie con 9.")
            return

        try:
            # Comprobar unicidad de DNI
            existente = cliente_model.buscar_cliente_por_dni(dni)
            if existente:
                self.vista.mostrar_error(f"El DNI {dni} ya se encuentra registrado.")
                return

            nuevo_id = cliente_model.insertar_cliente(nombres, dni, telefono)
            if nuevo_id:
                modal.destroy()  # Cierra la ventana emergente
                self.vista.mostrar_exito("Cliente registrado correctamente.")
                self.cargar_clientes()  # Actualiza la tabla automáticamente
            else:
                self.vista.mostrar_error("No se pudo registrar el cliente en la base de datos.")
        except Exception as error:
            self.vista.mostrar_error(f"Error al guardar cliente: {error}")