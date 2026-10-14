# Cola de turnos por nombre

Aplicación Flask para administrar una cola FIFO de personas. Solo se ingresan nombres; pueden escribirse o dictarse con el micrófono. La fila muestra el próximo turno a la izquierda y el final a la derecha.

## Ejecutar en Windows

1. Abre PowerShell en esta carpeta.
2. Activa el entorno: `.venv\Scripts\Activate.ps1`.
3. Si hace falta, instala Flask: `python -m pip install -r requirements.txt`.
4. Inicia el servidor: `python app.py`.
5. Abre `http://127.0.0.1:5001/`.

También puedes ejecutar directamente `.venv\Scripts\python.exe app.py`. Para dictar, usa un navegador compatible, conexión a internet y permite el acceso al micrófono.
