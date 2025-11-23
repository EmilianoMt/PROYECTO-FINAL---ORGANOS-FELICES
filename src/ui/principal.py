"""
Módulo principal de la interfaz gráfica de usuario.
"""
import os
from tkinter import messagebox
from PIL import Image
import customtkinter as ctk

from src.crud.crud import obtener_organos
from src.ui.agregar_organos import open_agregar
from src.ui.editar_organos import open_editar
from src.ui.eliminar_organos import confirmar_eliminar


def crear_tarjeta(padre, producto, idx, abrir_editar_cb, abrir_eliminar_cb):
    """Crear y colocar una tarjeta de producto en 'padre'."""
    tarjeta = ctk.CTkFrame(
        padre,
        fg_color="white",
        border_color="#E0E0E0",
        border_width=1,
        corner_radius=6,
    )
    tarjeta.grid(row=idx[0], column=idx[1], padx=12, pady=12, sticky="nsew")
    try:
        img_path = producto.get("imagen_path", "") or "estomago.png"
        if img_path and os.path.exists(img_path):
            with Image.open(img_path) as im:
                img = ctk.CTkImage(light_image=im.copy(), size=(180, 120))
            lbl = ctk.CTkLabel(tarjeta, image=img, text="")
            lbl.image = img
            lbl.pack(pady=(10, 6))
        else:
            raise FileNotFoundError
    except (FileNotFoundError, OSError):
        ctk.CTkLabel(
            tarjeta,
            text="[IMAGEN]",
            width=180,
            height=120,
            fg_color="#F0F0F0",
            text_color="#A0A0A0",
        ).pack(pady=(10, 6))

    ctk.CTkLabel(
        tarjeta, text=producto.get("nombre", ""), font=("Arial", 16, "bold")
    ).pack()
    ctk.CTkLabel(
        tarjeta,
        text=str(producto.get("precio", "")),
        font=("Arial", 14),
        text_color="#27AE60",
    ).pack()

    btns = ctk.CTkFrame(tarjeta, fg_color="white")
    btns.pack(pady=(6, 10))
    ctk.CTkButton(
        btns,
        text="📝 EDITAR",
        width=100,
        height=34,
        command=lambda: abrir_editar_cb(idx[2]),
    ).pack(side="left", padx=6)
    ctk.CTkButton(
        btns,
        text="🗑️ ELIMINAR",
        width=100,
        height=34,
        command=lambda: abrir_eliminar_cb(idx[2]),
    ).pack(side="left", padx=6)


def main():
    """Arranca la GUI principal (lista, agregar, editar y eliminar)."""
    datos_productos = []

    def load_from_db():
        nonlocal datos_productos
        datos_productos = obtener_organos() or []
        refresh_catalog()

    def abrir_agregar_callback():
        open_agregar(ventana, on_success=load_from_db)

    def abrir_editar_callback(index):
        try:
            producto = datos_productos[index]
        except IndexError:
            messagebox.showerror("Error", "Producto no encontrado")
            return
        open_editar(ventana, producto, on_success=load_from_db)

    def abrir_eliminar_callback(index):
        try:
            producto = datos_productos[index]
        except IndexError:
            messagebox.showerror("Error", "Producto no encontrado")
            return
        confirmar_eliminar(
            ventana,
            producto["id_organo"],
            producto.get("nombre", ""),
            on_success=load_from_db,
        )

    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("dark-blue")
    ventana = ctk.CTk(fg_color="white")
    ventana.title("ORGANOS FELICES - Catálogo")
    ventana.geometry("1100x700")

    header = ctk.CTkFrame(ventana, height=100, fg_color="#000000")
    header.pack(fill="x")
    ctk.CTkLabel(
        header,
        text="ORGANOS\nFELICES",
        font=("Arial Black", 28),
        text_color="white",
    ).place(relx=0.85, rely=0.5, anchor="center")

    products_container = ctk.CTkFrame(ventana, fg_color="white")
    products_container.pack(fill="both", expand=True, padx=20, pady=20)
    scrollable = ctk.CTkScrollableFrame(
        products_container, label_text="Catálogo", fg_color="white"
    )
    scrollable.pack(fill="both", expand=True)

    col_max = 3

    def refresh_catalog():
        for w in scrollable.winfo_children():
            w.destroy()
        if not datos_productos:
            ctk.CTkLabel(
                scrollable,
                text="AÚN NO HAY PRODUCTOS",
                font=("Arial Black", 20),
                text_color="#666666",
            ).pack(expand=True, pady=60)
            return

        for i, p in enumerate(datos_productos):
            r = i // col_max
            c = i % col_max
            crear_tarjeta(scrollable, p, (r, c, i), abrir_editar_callback, abrir_eliminar_callback)

        for i in range(col_max):
            scrollable.grid_columnconfigure(i, weight=1)

    btn_add = ctk.CTkButton(
        ventana,
        text="+",
        width=70,
        height=70,
        command=abrir_agregar_callback,
        fg_color="red",
    )
    btn_add.place(relx=0.97, rely=0.95, anchor="se")

    ventana.protocol(
        "WM_DELETE_WINDOW",
        lambda: (ventana.destroy() if messagebox.askyesno("Salir",  "¿Desea cerrar la aplicación?\nRecuerde que esto es confidencial," \
        "\nasegúrese que nadie lo observe." ) else None),

    )
    load_from_db()
    ventana.mainloop()
