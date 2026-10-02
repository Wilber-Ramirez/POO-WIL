from __future__ import annotations

from typing import Any


class Producto:
    def __init__(self, codigo: str, nombre: str, categoria: str, precio: float, stock: int = 0) -> None:
        self.codigo = self._campo(codigo, "codigo")
        self.nombre = self._campo(nombre, "nombre")
        self.categoria = self._campo(categoria, "categoria")
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        self.precio = float(precio)
        self.stock = int(stock)

    @staticmethod
    def _campo(valor: str, nombre: str) -> str:
        if valor is None or not str(valor).strip():
            raise ValueError(f"El campo {nombre} no puede estar vacio.")
        return str(valor).strip()

    def a_diccionario(self) -> dict[str, Any]:
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock,
        }

    @classmethod
    def desde_diccionario(cls, datos: dict[str, Any]) -> "Producto":
        return cls(
            datos["codigo"],
            datos["nombre"],
            datos["categoria"],
            float(datos["precio"]),
            int(datos.get("stock", 0)),
        )
