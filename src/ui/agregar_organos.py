"""
Módulo para la interfaz de agregar órganos.
"""
from tkinter import messagebox
import customtkinter as ctk
import pymysql
from src.crud.crud import insertar_organo

def open_agregar(parent, on_success=None):
    """
    Abre una ventana modal para agregar un órgano.
    """
    modal = ctk.CTkToplevel(parent)
    modal.title("Agregar órgano")
    modal.transient(parent)
    modal.grab_set()
    modal.geometry("700x480")

    ctk.CTkLabel(modal, text="AGREGAR ÓRGANO", font=("Arial Black", 20)).pack(pady=12)

    # Etiqueta + input Nombre
    ctk.CTkLabel(modal, text="Nombre:", anchor="w").pack(fill="x", padx=90)
    entry_nombre = ctk.CTkEntry(modal, width=520)
    entry_nombre.pack(pady=6)

    # Etiqueta + input Precio
    ctk.CTkLabel(modal, text="Precio:", anchor="w").pack(fill="x", padx=90)
    entry_precio = ctk.CTkEntry(modal, width=520)
    entry_precio.pack(pady=6)

    # Etiqueta + textarea Descripción
    ctk.CTkLabel(modal, text="Descripción:", anchor="w").pack(fill="x", padx=90)
    txt_desc = ctk.CTkTextbox(modal, width=520, height=140)
    txt_desc.pack(pady=6)

    def aceptar():
        nombre = entry_nombre.get().strip()
        precio = entry_precio.get().strip()
        desc = txt_desc.get("0.0", "end").strip()
        if not nombre:
            messagebox.showwarning("Validación", "El nombre no puede estar vacío.")
            return
        try:
            insertar_organo(nombre, precio, desc)
            if on_success:
                on_success()
            modal.destroy()
        except ValueError as err:
            messagebox.showwarning("Validación", str(err))
        except pymysql.MySQLError as err:
            messagebox.showerror("Error de base de datos", f"No se pudo insertar:\n{err}")

    # contenedor de botones centrado
    btns_container = ctk.CTkFrame(modal, fg_color="transparent")
    btns_container.pack(pady=12, anchor="center")

    ctk.CTkButton(
        btns_container,
        text="Aceptar",
        command=aceptar,
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
