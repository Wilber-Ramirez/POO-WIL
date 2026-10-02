from __future__ import annotations

from typing import Any


class Usuario:
    ROLES_VALIDOS = ("Administrador", "Empleado", "Cliente")

    def __init__(self, identificacion: str, nombre: str, correo: str, contrasena: str, rol: str = "Cliente") -> None:
        self.identificacion = self._campo(identificacion, "identificacion")
        self.nombre = self._campo(nombre, "nombre")
        self.correo = self._campo(correo, "correo")
        self.contrasena = self._campo(contrasena, "contrasena")
        self.rol = self._rol(rol)

    @staticmethod
    def _campo(valor: str, nombre: str) -> str:
        if valor is None or not str(valor).strip():
            raise ValueError(f"El campo {nombre} no puede estar vacio.")
        return str(valor).strip()

    @classmethod
    def _rol(cls, valor: str) -> str:
        rol = str(valor or "Cliente").strip().title()
        if rol not in cls.ROLES_VALIDOS:
            raise ValueError("El rol debe ser Administrador, Empleado o Cliente.")
        return rol

    def a_diccionario(self) -> dict[str, Any]:
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
            "contrasena": self.contrasena,
            "rol": self.rol,
        }

    @classmethod
    def desde_diccionario(cls, datos: dict[str, Any]) -> "Usuario":
        return cls(
            datos["identificacion"],
            datos["nombre"],
            datos["correo"],
            datos.get("contrasena", datos.get("password", "")),
            datos.get("rol", "Cliente"),
        )
