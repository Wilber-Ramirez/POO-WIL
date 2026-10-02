from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from restaurante_app.servicios.restaurante_servicio import RestauranteServicio


class LoginView(ttk.Frame):
    def __init__(self, master: tk.Tk, servicio: RestauranteServicio, acceso_correcto) -> None:
        super().__init__(master, padding=32)
        self.servicio = servicio
        self.acceso_correcto = acceso_correcto
        self.usuario = tk.StringVar()
        self.contrasena = tk.StringVar()
        self.columnconfigure(1, weight=1)
        self.icono = None
        try:
            self.icono = tk.PhotoImage(file=str(Path(__file__).resolve().parents[1] / "assets" / "icon.ppm"))
            ttk.Label(self, image=self.icono).grid(row=0, column=0, padx=(0, 10))
        except tk.TclError:
            pass
        ttk.Label(self, text="RESTAURANTE APP", style="Title.TLabel").grid(
            row=0, column=1, columnspan=2, sticky="w", pady=(0, 24)
        )
        ttk.Label(self, text="Usuario:").grid(row=1, column=0, sticky="w", pady=8)
        ttk.Entry(self, textvariable=self.usuario).grid(row=1, column=1, sticky="ew", pady=8)
        ttk.Label(self, text="Contraseña:").grid(row=2, column=0, sticky="w", pady=8)
        ttk.Entry(self, textvariable=self.contrasena, show="*").grid(row=2, column=1, sticky="ew", pady=8)
        ttk.Button(self, text="Iniciar sesión", command=self._iniciar).grid(
            row=3, column=0, columnspan=2, sticky="ew", pady=(20, 8)
        )
        ttk.Label(self, text="Demo: admin / admin123").grid(row=4, column=0, columnspan=2, sticky="w")
        self.bind("<Return>", lambda event: self._iniciar())
        self.bind("<Escape>", lambda event: self._limpiar())

    def _iniciar(self) -> None:
        usuario = self.servicio.autenticar(self.usuario.get(), self.contrasena.get())
        if usuario is None:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.")
            return
        self.acceso_correcto(usuario)

    def _limpiar(self) -> None:
        self.usuario.set("")
        self.contrasena.set("")
