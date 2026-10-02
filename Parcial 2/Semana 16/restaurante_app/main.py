from __future__ import annotations

import sys
import tkinter as tk
from pathlib import Path
from tkinter import ttk

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from restaurante_app.servicios.restaurante_servicio import RestauranteServicio
from restaurante_app.ui.login_view import LoginView
from restaurante_app.ui.main_view import MainView


class Aplicacion:
    def __init__(self) -> None:
        self.raiz = tk.Tk()
        self.raiz.title("Restaurante App - Semana 16")
        self.raiz.geometry("1150x700")
        self.raiz.minsize(900, 560)
        estilo = ttk.Style()
        estilo.configure("Title.TLabel", font=("Segoe UI", 18, "bold"))
        estilo.configure("Heading.TLabel", font=("Segoe UI", 14, "bold"))
        self.servicio = RestauranteServicio()
        self.vista = None
        self.mostrar_login()

    def _cambiar_vista(self, vista) -> None:
        if self.vista is not None:
            self.vista.destroy()
        self.vista = vista
        self.vista.pack(fill="both", expand=True)

    def mostrar_login(self) -> None:
        self._cambiar_vista(LoginView(self.raiz, self.servicio, self.mostrar_principal))

    def mostrar_principal(self, usuario) -> None:
        self._cambiar_vista(MainView(self.raiz, self.servicio, usuario))

    def ejecutar(self) -> None:
        self.raiz.mainloop()


def main() -> None:
    Aplicacion().ejecutar()


if __name__ == "__main__":
    main()
