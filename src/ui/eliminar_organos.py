"""
Módulo para la interfaz de eliminar órganos.
"""
from tkinter import messagebox
import customtkinter as ctk
import pymysql
from src.crud.crud import eliminar_organo

def confirmar_eliminar(parent, id_organo, nombre, on_success=None):
    """
    Abre un modal para confirmar la eliminación de un órgano.
    """
    modal = ctk.CTkToplevel(parent)
    modal.title("Eliminar órgano")
    modal.transient(parent)
    modal.grab_set()
    modal.geometry("480x180")

    ctk.CTkLabel(modal, text=f"¿Eliminar '{nombre}'?", font=("Arial Black", 14)).pack(pady=10)

    def confirmar():
        try:
            eliminar_organo(id_organo)
            if on_success:
                on_success()
            modal.destroy()
        except pymysql.MySQLError as err:
            messagebox.showerror("Error de base de datos", f"No se pudo eliminar:\n{err}")

    btns_container = ctk.CTkFrame(modal, fg_color="transparent")
    btns_container.pack(pady=12, anchor="center")

    ctk.CTkButton(
        btns_container,
        text="Aceptar",
        command=confirmar,
        fg_color="#008A07",
        width=120,
        height=34,
    ).pack(side="left", padx=12)

    ctk.CTkButton(
        btns_container,
        text="Cancelar",
        command=modal.destroy,
        fg_color="#C90000",
        width=120,
        height=34,
    ).pack(side="left", padx=12)

    modal.wait_window()
