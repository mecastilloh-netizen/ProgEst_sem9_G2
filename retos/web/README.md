# Gestor de solicitudes

Aplicación Flask de aprendizaje con una cola de pendientes (FIFO) y una pila de atenciones (LIFO). Los datos viven en memoria y se reinician al detener el servidor.

## Ejecutar

El entorno `.venv` ya está creado en esta carpeta. En Windows, desde PowerShell, ejecuta:

```powershell
.\.venv\Scripts\python.exe app.py
```

Abre <http://127.0.0.1:5000/>. No abras `templates/index.html` directamente: los bloques `{{ ... }}` y `{% ... %}` solo se procesan cuando Flask sirve la página.

Si vuelves a crear el entorno, usa `py -m venv .venv` y `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`. En macOS o Linux, usa `python3 -m venv .venv`, `source .venv/bin/activate`, `pip install -r requirements.txt` y `python app.py`.

Las rutas de registro, atención, cancelación y deshacer usan POST. La búsqueda por ID usa GET.
