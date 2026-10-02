# Semana 16 - Restaurante App con eventos y gestión de usuarios

Esta versión evoluciona la aplicación del restaurante conservando la estructura modular de semanas anteriores y adicionando la gestión de usuarios desde la interfaz mediante eventos de Tkinter.

## Objetivo

La app mantiene la navegación por productos, ventas y usuarios, pero en la sección de usuarios se aplica el flujo de interacción:

usuario -> evento -> bind() -> callback -> servicio -> persistencia -> respuesta visual

Se trabaja con un formulario y un Treeview para registrar, consultar, actualizar y eliminar usuarios, con roles básicos y validaciones del servicio.

## Cambios principales

- Se incorporó el atributo `rol` al modelo `Usuario` con valores: Administrador, Empleado y Cliente.
- La gestión de usuarios se realiza desde la vista principal únicamente por usuarios con rol Administrador.
- Se implementó un `Treeview` para listar usuarios con identificación, nombre, correo y rol.
- El evento `<<TreeviewSelect>>` carga los datos del usuario seleccionado en el formulario.
- El evento `<Return>` reutiliza la acción de registro para confirmar el ingreso del usuario.
- El evento `<Escape>` limpia el formulario y la selección actual.
- El evento `<<ComboboxSelected>>` responde al cambio del rol seleccionado.
- Los botones principales usan `command=` y las acciones de teclado se gestionan con `bind()`.
- Las validaciones y persistencia se manejan dentro de `RestauranteServicio` y `ArchivoServicio`.

## Estructura del proyecto

- `restaurante_app/main.py`: punto de entrada de la interfaz.
- `restaurante_app/modelos/`: clases `Producto`, `Usuario` y `Venta`.
- `restaurante_app/servicios/`: lógica de negocio y persistencia.
- `restaurante_app/ui/`: vistas `LoginView` y `MainView`.
- `restaurante_app/datos/`: JSON de productos, usuarios y ventas.
- `restaurante_app/assets/`: íconos y recursos visuales.

## Cómo ejecutar

Desde la carpeta `Semana 16`:

```bash
python main.py
```

o desde la carpeta `Semana 16/restaurante_app`:

```bash
python main.py
```

## Usuarios de prueba

- Usuario: `admin`
- Contraseña: `admin123`
- Rol: `Administrador`

## Archivos JSON

Los datos se conservan en archivos JSON para simular persistencia local:

- `restaurante_app/datos/usuarios.json`
- `restaurante_app/datos/productos.json`
- `restaurante_app/datos/ventas.json`

## Consideraciones

La lógica de negocio y la persistencia no se implementan dentro de la interfaz. La vista solo coordina la interacción con el usuario y delega las operaciones en el servicio.
