from __future__ import annotations

from datetime import datetime
from typing import Any


class Venta:
    """Relaciona un usuario y un producto con la fecha de la operación."""

    def __init__(self, usuario_id: str, producto_codigo: str, fecha: str | None = None) -> None:
        self.usuario_id = self._campo(usuario_id, "usuario")
        self.producto_codigo = self._campo(producto_codigo, "producto")
        self.fecha = fecha or datetime.now().isoformat(timespec="seconds")

    @staticmethod
    def _campo(valor: str, nombre: str) -> str:
        if valor is None or not str(valor).strip():
            raise ValueError(f"Debe indicar un {nombre}.")
        return str(valor).strip()

    def a_diccionario(self) -> dict[str, Any]:
        return {
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "fecha": self.fecha,
        }

    @classmethod
    def desde_diccionario(cls, datos: dict[str, Any]) -> "Venta":
        return cls(datos["usuario_id"], datos["producto_codigo"], datos["fecha"])
