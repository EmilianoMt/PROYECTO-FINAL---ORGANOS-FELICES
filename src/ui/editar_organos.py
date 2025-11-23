"""
Módulo para la interfaz de editar órganos.
"""
from tkinter import messagebox
import customtkinter as ctk
import pymysql
from src.crud.crud import actualizar_organo

def open_editar(parent, producto: dict, on_success=None):
    """
    Abre un modal para editar un órgano existente.
    """
    modal = ctk.CTkToplevel(parent)
    modal.title("Editar órgano")
    modal.transient(parent)
    modal.grab_set()
    modal.geometry("640x420")

    ctk.CTkLabel(modal, text="Editar órgano", font=("Arial Black", 18)).pack(pady=10)
    entry_nombre = ctk.CTkEntry(modal, width=520)
    entry_nombre.insert(0, producto.get("nombre", ""))
    entry_nombre.pack(pady=6)
    entry_precio = ctk.CTkEntry(modal, width=520)
    entry_precio.insert(0, str(producto.get("precio", "")))
    entry_precio.pack(pady=6)
    txt_desc = ctk.CTkTextbox(modal, width=520, height=160)
    txt_desc.insert("0.0", producto.get("descripcion", ""))
    txt_desc.pack(pady=6)

    def aceptar():
        nombre = entry_nombre.get().strip()
        precio = entry_precio.get().strip()
        desc = txt_desc.get("0.0", "end").strip()
        if not nombre:
            messagebox.showwarning("Validación", "El nombre no puede estar vacío.")
            return
        try:
            actualizar_organo(producto["id_organo"], nombre, precio, desc)
            if on_success:
                on_success()
            modal.destroy()
        except ValueError as err:
            # errores de validación lanzados por la capa de negocio
            messagebox.showwarning("Validación", str(err))
        except pymysql.MySQLError as err:
            # errores relacionados con la base de datos
            messagebox.showerror("Error de base de datos", f"No se pudo actualizar:\n{err}")

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
