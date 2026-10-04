import customtkinter as ctk
from tkinter import messagebox

class LoginView(ctk.CTkFrame):
    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Contenedor central moderno
        self.frame_centro = ctk.CTkFrame(self, corner_radius=20)
        self.frame_centro.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.frame_centro.grid_columnconfigure(0, weight=1)

        # Título / Branding del Rincón Criollo
        self.lbl_titulo = ctk.CTkLabel(self.frame_centro, text="El Rincón Criollo", font=("Helvetica", 24, "bold"))
        self.lbl_titulo.grid(row=0, column=0, padx=20, pady=(40, 20))

        # Campo de Usuario con sugerencia @gmail.com dentro
        self.entry_usuario = ctk.CTkEntry(self.frame_centro, placeholder_text="usuario@gmail.com", width=280, height=40)
        self.entry_usuario.grid(row=1, column=0, padx=20, pady=10)

        # Campo de Contraseña
        self.entry_password = ctk.CTkEntry(self.frame_centro, placeholder_text="Contraseña", show="*", width=280, height=40)
        self.entry_password.grid(row=2, column=0, padx=20, pady=10)

        # Botón estilizado
        self.btn_ingresar = ctk.CTkButton(self.frame_centro, text="Ingresar al Sistema", width=280, height=40, command=self._clic_ingresar)
        self.btn_ingresar.grid(row=3, column=0, padx=20, pady=(20, 40))

    def _clic_ingresar(self):
        if self.controlador and hasattr(self.controlador, "manejar_login"):
            self.controlador.manejar_login()

    def get_usuario(self) -> str:
        texto_usuario = self.entry_usuario.get().strip()
        if not texto_usuario:
            return ""
        if "@" not in texto_usuario:
            return f"{texto_usuario}@gmail.com"
        return texto_usuario

    def get_password(self) -> str:
        return self.entry_password.get()

    def limpiar(self):
        self.entry_usuario.delete(0, 'end')
        self.entry_password.delete(0, 'end')

    def mostrar_error(self, mensaje: str):
        messagebox.showerror("Error de Autenticación", mensaje)

    def mostrar_exito(self, mensaje: str):
        messagebox.showinfo("Éxito", mensaje)