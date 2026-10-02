from __future__ import annotations

from pathlib import Path

from restaurante_app.modelos.producto import Producto
from restaurante_app.modelos.usuario import Usuario
from restaurante_app.modelos.venta import Venta
from restaurante_app.servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    def __init__(self, ruta_datos: str | Path | None = None) -> None:
        base = Path(__file__).resolve().parents[1]
        self.archivos = ArchivoServicio(ruta_datos or base / "datos")
        self._productos = self.archivos.cargar_productos()
        self._usuarios = self.archivos.cargar_usuarios()
        self._ventas = self.archivos.cargar_ventas()

    def autenticar(self, identificacion: str, contrasena: str) -> Usuario | None:
        clave = (identificacion or "").strip()
        password = (contrasena or "").strip()
        return next((u for u in self._usuarios if u.identificacion == clave and u.contrasena == password), None)

    def listar_usuarios(self) -> list[Usuario]:
        return list(self._usuarios)

    def buscar_usuario(self, identificacion: str) -> Usuario | None:
        clave = (identificacion or "").strip()
        return next((u for u in self._usuarios if u.identificacion == clave), None)

    def listar_productos(self) -> list[Producto]:
        return list(self._productos)

    def buscar_producto(self, codigo: str) -> Producto | None:
        clave = (codigo or "").strip()
        return next((p for p in self._productos if p.codigo == clave), None)

    def registrar_producto(self, producto: Producto) -> bool:
        if self.buscar_producto(producto.codigo):
            return False
        self._productos.append(producto)
        self.archivos.guardar_productos(self._productos)
        return True

    def actualizar_producto(self, codigo: str, nombre: str, categoria: str,
                            precio: float, stock: int) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        producto.nombre = Producto._campo(nombre, "nombre")
        producto.categoria = Producto._campo(categoria, "categoria")
        if precio < 0 or stock < 0:
            raise ValueError("Precio y stock deben ser mayores o iguales a cero.")
        producto.precio = float(precio)
        producto.stock = int(stock)
        self.archivos.guardar_productos(self._productos)
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        self._productos.remove(producto)
        self.archivos.guardar_productos(self._productos)
        return True

    def registrar_usuario(self, usuario: Usuario) -> bool:
        if self.buscar_usuario(usuario.identificacion) is not None:
            return False
        self._usuarios.append(usuario)
        self.archivos.guardar_usuarios(self._usuarios)
        return True

    def actualizar_usuario(self, identificacion: str, nombre: str, correo: str,
                           contrasena: str, rol: str) -> bool:
        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            return False
        usuario.nombre = Usuario._campo(nombre, "nombre")
        usuario.correo = Usuario._campo(correo, "correo")
        if contrasena is not None and str(contrasena).strip():
            usuario.contrasena = Usuario._campo(contrasena, "contrasena")
        usuario.rol = Usuario._rol(rol)
        self.archivos.guardar_usuarios(self._usuarios)
        return True

    def eliminar_usuario(self, identificacion: str) -> bool:
        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            return False
        if usuario.rol == "Administrador":
            raise ValueError("El usuario administrador no puede eliminarse.")
        self._usuarios.remove(usuario)
        self.archivos.guardar_usuarios(self._usuarios)
        return True

    def listar_ventas(self) -> list[Venta]:
        return list(self._ventas)

    def registrar_venta(self, usuario_id: str, producto_codigo: str) -> Venta:
        usuario = self.buscar_usuario(usuario_id)
        producto = self.buscar_producto(producto_codigo)
        if usuario is None:
            raise ValueError("El usuario seleccionado no existe.")
        if producto is None:
            raise ValueError("El producto seleccionado no existe.")
        venta = Venta(usuario.identificacion, producto.codigo)
        self._ventas.append(venta)
        self.archivos.guardar_ventas(self._ventas)
        return venta
