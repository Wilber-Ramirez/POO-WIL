from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from restaurante_app.modelos.producto import Producto
from restaurante_app.modelos.usuario import Usuario
from restaurante_app.servicios.restaurante_servicio import RestauranteServicio


class MainView(ttk.Frame):
    def __init__(self, master: tk.Tk, servicio: RestauranteServicio, usuario: Usuario) -> None:
        super().__init__(master, padding=16)
        self.servicio = servicio
        self.usuario = usuario
        self.logo = None
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self._crear_cabecera()
        self._crear_navegacion()
        self.contenido = ttk.Frame(self)
        self.contenido.grid(row=1, column=1, sticky="nsew", padx=(16, 0))
        self.mostrar_productos()

    def _crear_cabecera(self) -> None:
        cabecera = ttk.Frame(self)
        cabecera.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 16))
        ruta_logo = Path(__file__).resolve().parents[1] / "assets" / "logo.ppm"
        try:
            self.logo = tk.PhotoImage(file=str(ruta_logo))
            ttk.Label(cabecera, image=self.logo).pack(side="left", padx=(0, 10))
        except tk.TclError:
            pass
        ttk.Label(
            cabecera,
            text=f"Restaurante App | Bienvenido, {self.usuario.nombre} ({self.usuario.rol})",
            style="Title.TLabel",
        ).pack(side="left")

    def _crear_navegacion(self) -> None:
        menu = ttk.LabelFrame(self, text="Navegación", padding=10)
        menu.grid(row=1, column=0, sticky="ns")
        ttk.Button(menu, text="Productos", command=self.mostrar_productos).pack(fill="x", pady=4)
        self.boton_usuarios = ttk.Button(menu, text="Usuarios", command=self.mostrar_usuarios)
        self.boton_usuarios.pack(fill="x", pady=4)
        if self.usuario.rol != "Administrador":
            self.boton_usuarios.configure(state="disabled")
        ttk.Button(menu, text="Ventas", command=self.mostrar_ventas).pack(fill="x", pady=4)

    def _limpiar(self) -> None:
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def mostrar_usuarios(self) -> None:
        if self.usuario.rol != "Administrador":
            messagebox.showwarning("Acceso restringido", "Solo el administrador puede gestionar usuarios.")
            return
        self._limpiar()
        ttk.Label(self.contenido, text="Gestión de usuarios", style="Heading.TLabel").pack(anchor="w")

        self.identificacion_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.correo_var = tk.StringVar()
        self.contrasena_var = tk.StringVar()
        self.rol_var = tk.StringVar(value="Cliente")

        formulario = ttk.LabelFrame(self.contenido, text="Datos del usuario", padding=12)
        formulario.pack(fill="x", pady=(12, 10))

        self.identificacion_entry = ttk.Entry(formulario, textvariable=self.identificacion_var, width=24)
        self.nombre_entry = ttk.Entry(formulario, textvariable=self.nombre_var, width=24)
        self.correo_entry = ttk.Entry(formulario, textvariable=self.correo_var, width=24)
        self.contrasena_entry = ttk.Entry(formulario, textvariable=self.contrasena_var, show="*", width=24)
        self.rol_combo = ttk.Combobox(
            formulario,
            textvariable=self.rol_var,
            values=["Administrador", "Empleado", "Cliente"],
            state="readonly",
            width=22,
        )
        self.rol_combo.set("Cliente")

        campos = [
            ("Identificación", self.identificacion_entry, 0),
            ("Nombre", self.nombre_entry, 1),
            ("Correo", self.correo_entry, 2),
            ("Contraseña", self.contrasena_entry, 3),
            ("Rol", self.rol_combo, 4),
        ]
        for etiqueta, widget, columna in campos:
            ttk.Label(formulario, text=etiqueta).grid(row=0, column=columna, sticky="w", padx=4)
            widget.grid(row=1, column=columna, padx=4, pady=(4, 0), sticky="ew")

        acciones = ttk.Frame(self.contenido)
        acciones.pack(fill="x", pady=(0, 10))
        ttk.Button(acciones, text="Registrar", command=self.registrar_usuario).pack(side="left", padx=3)
        ttk.Button(acciones, text="Actualizar", command=self.actualizar_usuario).pack(side="left", padx=3)
        ttk.Button(acciones, text="Eliminar", command=self.eliminar_usuario).pack(side="left", padx=3)
        ttk.Button(acciones, text="Limpiar", command=self.limpiar_formulario).pack(side="left", padx=3)

        self.tabla_usuarios = ttk.Treeview(
            self.contenido,
            columns=("identificacion", "nombre", "correo", "rol"),
            show="headings",
        )
        for columna, texto in (
            ("identificacion", "Identificación"),
            ("nombre", "Nombre"),
            ("correo", "Usuario"),
            ("rol", "Rol"),
        ):
            self.tabla_usuarios.heading(columna, text=texto)
            self.tabla_usuarios.column(columna, width=170)
        self.tabla_usuarios.pack(fill="both", expand=True)
        self.actualizar_tabla_usuarios()

        self.bind("<Return>", self._evento_registro)
        self.bind("<Escape>", self._evento_limpiar)
        self.tabla_usuarios.bind("<<TreeviewSelect>>", self._cargar_usuario_desde_tabla)
        self.tabla_usuarios.bind("<Escape>", self._evento_limpiar)
        self.rol_combo.bind("<<ComboboxSelected>>", self._evento_cambio_rol)
        self.identificacion_entry.bind("<Return>", self._evento_registro)
        self.nombre_entry.bind("<Return>", self._evento_registro)
        self.correo_entry.bind("<Return>", self._evento_registro)
        self.contrasena_entry.bind("<Return>", self._evento_registro)
        self.rol_combo.bind("<Return>", self._evento_registro)
        self.identificacion_entry.bind("<Escape>", self._evento_limpiar)
        self.nombre_entry.bind("<Escape>", self._evento_limpiar)
        self.correo_entry.bind("<Escape>", self._evento_limpiar)
        self.contrasena_entry.bind("<Escape>", self._evento_limpiar)
        self.rol_combo.bind("<Escape>", self._evento_limpiar)

    def _evento_registro(self, _event=None) -> None:
        self.registrar_usuario()

    def _evento_limpiar(self, _event=None) -> None:
        self.limpiar_formulario()

    def _evento_cambio_rol(self, _event=None) -> None:
        self.rol_var.set(self.rol_var.get())

    def _cargar_usuario_desde_tabla(self, _event=None) -> None:
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            return
        valores = self.tabla_usuarios.item(seleccion[0], "values")
        if not valores:
            return
        usuario = self.servicio.buscar_usuario(valores[0])
        if usuario is None:
            return
        self.identificacion_var.set(usuario.identificacion)
        self.nombre_var.set(usuario.nombre)
        self.correo_var.set(usuario.correo)
        self.contrasena_var.set(usuario.contrasena)
        self.rol_var.set(usuario.rol)

    def registrar_usuario(self) -> None:
        try:
            identificacion = self.identificacion_var.get().strip()
            nombre = self.nombre_var.get().strip()
            correo = self.correo_var.get().strip()
            contrasena = self.contrasena_var.get().strip()
            rol = self.rol_var.get().strip()
            if not identificacion or not nombre or not correo or not contrasena:
                raise ValueError("Identificación, nombre, correo y contraseña son obligatorios.")
            usuario = Usuario(identificacion, nombre, correo, contrasena, rol)
            if not self.servicio.registrar_usuario(usuario):
                raise ValueError("Ya existe un usuario con esa identificación.")
            self._resultado_usuario("Usuario registrado correctamente.")
            self.limpiar_formulario()
        except (ValueError, TypeError) as exc:
            messagebox.showerror("Datos inválidos", str(exc))

    def actualizar_usuario(self) -> None:
        try:
            identificacion = self.identificacion_var.get().strip()
            if not identificacion:
                raise ValueError("Debe seleccionar un usuario para actualizar.")
            nombre = self.nombre_var.get().strip()
            correo = self.correo_var.get().strip()
            contrasena = self.contrasena_var.get().strip()
            rol = self.rol_var.get().strip()
            if not nombre or not correo:
                raise ValueError("Nombre y correo son obligatorios.")
            if not self.servicio.actualizar_usuario(identificacion, nombre, correo, contrasena, rol):
                raise ValueError("No se encontró el usuario indicado.")
            self._resultado_usuario("Usuario actualizado correctamente.")
            self.limpiar_formulario()
        except (ValueError, TypeError) as exc:
            messagebox.showerror("Datos inválidos", str(exc))

    def eliminar_usuario(self) -> None:
        identificacion = self.identificacion_var.get().strip()
        if not identificacion:
            messagebox.showerror("Datos inválidos", "Seleccione un usuario para eliminar.")
            return
        if identificacion == self.usuario.identificacion:
            messagebox.showwarning("Eliminación", "La cuenta administrativa autenticada no puede eliminarse.")
            return
        try:
            if not self.servicio.eliminar_usuario(identificacion):
                raise ValueError("No se encontró el usuario indicado.")
            self._resultado_usuario("Usuario eliminado correctamente.")
            self.limpiar_formulario()
        except ValueError as exc:
            messagebox.showerror("Eliminación", str(exc))

    def limpiar_formulario(self) -> None:
        if hasattr(self, "identificacion_var"):
            self.identificacion_var.set("")
            self.nombre_var.set("")
            self.correo_var.set("")
            self.contrasena_var.set("")
            self.rol_var.set("Cliente")
            if hasattr(self, "tabla_usuarios"):
                for item in list(self.tabla_usuarios.selection()):
                    self.tabla_usuarios.selection_remove(item)

    def _resultado_usuario(self, mensaje: str) -> None:
        messagebox.showinfo("Operación completada", mensaje)
        self.actualizar_tabla_usuarios()

    def actualizar_tabla_usuarios(self) -> None:
        if not hasattr(self, "tabla_usuarios"):
            return
        for fila in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(fila)
        for usuario in self.servicio.listar_usuarios():
            self.tabla_usuarios.insert(
                "",
                "end",
                values=(usuario.identificacion, usuario.nombre, usuario.correo, usuario.rol),
            )

    def mostrar_productos(self) -> None:
        self._limpiar()
        self.codigo = tk.StringVar()
        self.nombre = tk.StringVar()
        self.categoria = tk.StringVar()
        self.precio = tk.StringVar()
        self.stock = tk.StringVar()
        ttk.Label(self.contenido, text="Gestión de productos", style="Heading.TLabel").pack(anchor="w")
        formulario = ttk.LabelFrame(self.contenido, text="Datos del producto", padding=12)
        formulario.pack(fill="x", pady=(12, 10))
        campos = (
            ("Código", self.codigo),
            ("Nombre", self.nombre),
            ("Categoría", self.categoria),
            ("Precio", self.precio),
            ("Stock", self.stock),
        )
        for indice, (etiqueta, variable) in enumerate(campos):
            ttk.Label(formulario, text=etiqueta).grid(row=0, column=indice, sticky="w", padx=4)
            ttk.Entry(formulario, textvariable=variable, width=16).grid(row=1, column=indice, padx=4, pady=(4, 0))
        acciones = ttk.Frame(self.contenido)
        acciones.pack(fill="x", pady=(0, 10))
        ttk.Button(acciones, text="Registrar", command=self.registrar).pack(side="left", padx=3)
        ttk.Button(acciones, text="Cargar / consultar", command=self.cargar).pack(side="left", padx=3)
        ttk.Button(acciones, text="Actualizar", command=self.actualizar).pack(side="left", padx=3)
        ttk.Button(acciones, text="Eliminar", command=self.eliminar).pack(side="left", padx=3)
        self.tabla = ttk.Treeview(
            self.contenido,
            columns=("codigo", "nombre", "categoria", "precio", "stock"),
            show="headings",
        )
        for columna, texto in (
            ("codigo", "Código"),
            ("nombre", "Nombre"),
            ("categoria", "Categoría"),
            ("precio", "Precio"),
            ("stock", "Stock"),
        ):
            self.tabla.heading(columna, text=texto)
            self.tabla.column(columna, width=120)
        self.tabla.pack(fill="both", expand=True)
        self.actualizar_tabla()

    def _datos(self) -> tuple[str, str, str, float, int]:
        if not self.codigo.get().strip():
            raise ValueError("El código es obligatorio.")
        return (
            self.codigo.get().strip(),
            self.nombre.get().strip(),
            self.categoria.get().strip(),
            float(self.precio.get()),
            int(self.stock.get()),
        )

    def registrar(self) -> None:
        try:
            codigo, nombre, categoria, precio, stock = self._datos()
            producto = Producto(codigo, nombre, categoria, precio, stock)
            if not self.servicio.registrar_producto(producto):
                raise ValueError("Ya existe un producto con ese código.")
            self._resultado("Producto registrado correctamente.")
        except (ValueError, TypeError) as exc:
            messagebox.showerror("Datos inválidos", str(exc))

    def cargar(self) -> None:
        producto = self.servicio.buscar_producto(self.codigo.get())
        if producto is None:
            messagebox.showwarning("Consulta", "No se encontró el producto.")
            return
        self.nombre.set(producto.nombre)
        self.categoria.set(producto.categoria)
        self.precio.set(str(producto.precio))
        self.stock.set(str(producto.stock))
        messagebox.showinfo("Consulta", "Producto cargado en el formulario.")

    def actualizar(self) -> None:
        try:
            codigo, nombre, categoria, precio, stock = self._datos()
            if not self.servicio.actualizar_producto(codigo, nombre, categoria, precio, stock):
                raise ValueError("No se encontró el producto.")
            self._resultado("Producto actualizado correctamente.")
        except (ValueError, TypeError) as exc:
            messagebox.showerror("Datos inválidos", str(exc))

    def eliminar(self) -> None:
        if not self.codigo.get().strip():
            messagebox.showerror("Datos inválidos", "Indique el código del producto.")
            return
        if not self.servicio.eliminar_producto(self.codigo.get()):
            messagebox.showwarning("Eliminación", "No se encontró el producto.")
            return
        self._resultado("Producto eliminado correctamente.")

    def _resultado(self, mensaje: str) -> None:
        messagebox.showinfo("Operación completada", mensaje)
        self.actualizar_tabla()

    def actualizar_tabla(self) -> None:
        if not hasattr(self, "tabla"):
            return
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        for producto in self.servicio.listar_productos():
            self.tabla.insert(
                "",
                "end",
                values=(producto.codigo, producto.nombre, producto.categoria, f"{producto.precio:.2f}", producto.stock),
            )

    def mostrar_ventas(self) -> None:
        self._limpiar()
        ttk.Label(self.contenido, text="Registrar ventas", style="Heading.TLabel").pack(anchor="w")
        formulario = ttk.LabelFrame(self.contenido, text="Nueva venta", padding=12)
        formulario.pack(fill="x", pady=(12, 10))
        self.usuario_venta = tk.StringVar()
        self.producto_venta = tk.StringVar()
        usuarios = self.servicio.listar_usuarios()
        productos = self.servicio.listar_productos()

        ttk.Label(formulario, text="Usuario").grid(row=0, column=0, sticky="w", padx=4)
        ttk.Label(formulario, text="Producto").grid(row=0, column=1, sticky="w", padx=4)
        ttk.Combobox(
            formulario,
            textvariable=self.usuario_venta,
            state="readonly",
            values=[f"{u.identificacion} - {u.nombre}" for u in usuarios],
            width=28,
        ).grid(row=1, column=0, padx=4, pady=4)
        ttk.Combobox(
            formulario,
            textvariable=self.producto_venta,
            state="readonly",
            values=[f"{p.codigo} - {p.nombre}" for p in productos],
            width=28,
        ).grid(row=1, column=1, padx=4, pady=4)
        ttk.Button(formulario, text="Registrar venta", command=self.registrar_venta).grid(row=1, column=2, padx=8, pady=4)

        self.tabla_ventas = ttk.Treeview(
            self.contenido,
            columns=("fecha", "usuario", "producto"),
            show="headings",
        )
        for columna, texto in (("fecha", "Fecha"), ("usuario", "Usuario"), ("producto", "Producto")):
            self.tabla_ventas.heading(columna, text=texto)
            self.tabla_ventas.column(columna, width=220)
        self.tabla_ventas.pack(fill="both", expand=True)
        self.actualizar_tabla_ventas()

    def registrar_venta(self) -> None:
        if not self.usuario_venta.get() or not self.producto_venta.get():
            messagebox.showwarning("Venta", "Seleccione un usuario y un producto.")
            return
        usuario_id = self.usuario_venta.get().split(" - ", 1)[0]
        producto_codigo = self.producto_venta.get().split(" - ", 1)[0]
        try:
            venta = self.servicio.registrar_venta(usuario_id, producto_codigo)
        except ValueError as exc:
            messagebox.showerror("Venta no registrada", str(exc))
            return
        self.actualizar_tabla_ventas()
        messagebox.showinfo("Venta registrada", f"Venta guardada el {venta.fecha}.")

    def actualizar_tabla_ventas(self) -> None:
        if not hasattr(self, "tabla_ventas"):
            return
        for fila in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(fila)
        usuarios = {u.identificacion: u.nombre for u in self.servicio.listar_usuarios()}
        productos = {p.codigo: p.nombre for p in self.servicio.listar_productos()}
        for venta in self.servicio.listar_ventas():
            self.tabla_ventas.insert(
                "",
                "end",
                values=(venta.fecha, usuarios.get(venta.usuario_id, venta.usuario_id), productos.get(venta.producto_codigo, venta.producto_codigo)),
            )
