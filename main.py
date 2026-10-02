import customtkinter as ctk

# TODO: Importar los modelos (Jybran) y vistas (Bolivar) cuando estén listos
# from views.login_view import LoginView
# from models.usuario_model import UsuarioModel
# from controllers.login_controller import LoginController

def main():
    # Configuración de la interfaz moderna
    ctk.set_appearance_mode("System")  # Soporte para modo oscuro/claro
    ctk.set_default_color_theme("blue")

    # Inicialización de la ventana principal
    app = ctk.CTk()
    app.title("El Rincón Criollo - Sistema de Gestión")
    app.geometry("800x600")

    # TODO: Lógica de inicialización MVC
    # modelo_usuario = UsuarioModel()
    # vista_login = LoginView(app)
    # controlador_login = LoginController(vista_login, modelo_usuario)
    
    # Mensaje temporal de prueba para tu entorno
    lbl_prueba = ctk.CTkLabel(
        app, 
        text="¡Entorno de Israel configurado y listo para programar!", 
        font=("Arial", 24, "bold")
    )
    lbl_prueba.pack(expand=True)

    # Iniciar el ciclo de la aplicación
    app.mainloop()

if __name__ == "__main__":
    main()