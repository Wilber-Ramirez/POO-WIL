from __future__ import annotations

import json
from pathlib import Path
from typing import TypeVar

from restaurante_app.modelos.producto import Producto
from restaurante_app.modelos.usuario import Usuario
from restaurante_app.modelos.venta import Venta

T = TypeVar("T")


class ArchivoServicio:
    def __init__(self, directorio: str | Path) -> None:
        self.directorio = Path(directorio)
        self.directorio.mkdir(parents=True, exist_ok=True)

    def _cargar(self, nombre: str, constructor: type[T]) -> list[T]:
        ruta = self.directorio / nombre
        if not ruta.exists():
            return []
        try:
            datos = json.loads(ruta.read_text(encoding="utf-8"))
            return [constructor.desde_diccionario(item) for item in datos if isinstance(item, dict)]
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"No se pudo leer {nombre}: {exc}") from exc

    def _guardar(self, nombre: str, registros: list[T]) -> None:
        ruta = self.directorio / nombre
        datos = [registro.a_diccionario() for registro in registros]
        ruta.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")

    def cargar_productos(self) -> list[Producto]:
        return self._cargar("productos.json", Producto)

    def guardar_productos(self, productos: list[Producto]) -> None:
        self._guardar("productos.json", productos)

    def cargar_usuarios(self) -> list[Usuario]:
        return self._cargar("usuarios.json", Usuario)

    def guardar_usuarios(self, usuarios: list[Usuario]) -> None:
        self._guardar("usuarios.json", usuarios)

    def cargar_ventas(self) -> list[Venta]:
        return self._cargar("ventas.json", Venta)

    def guardar_ventas(self, ventas: list[Venta]) -> None:
        self._guardar("ventas.json", ventas)
