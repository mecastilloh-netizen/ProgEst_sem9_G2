# Visualizador de pilas con Flask

Aplicación educativa para practicar pilas LIFO de palabras e imágenes. Al entrar por primera vez se elige una de las dos opciones; cada pila se conserva por separado en la sesión del navegador. Flask gestiona las operaciones, Pillow procesa las imágenes y Bootstrap 5.3.8 da formato adaptable. No hay archivos CSS propios; JavaScript aplica los degradados, anima los botones y actualiza la visualización y el código Python.

## Requisitos

- Python 3.10 o posterior.
- Conexión a internet para cargar Bootstrap desde jsDelivr.

## Instalación y ejecución

1. Abre una terminal en la carpeta del proyecto.
2. El entorno virtual `.venv` ya está creado. Si necesitas recrearlo, usa `py -3.12 -m venv .venv`.
3. Actívalo en PowerShell: `.venv\Scripts\Activate.ps1` (en CMD: `.venv\Scripts\activate.bat`).
4. Las dependencias ya están instaladas en `.venv`. Para instalarlas en otro equipo, ejecuta `python -m pip install -r requirements.txt`.
5. Ejecuta la aplicación: `python app.py`.
6. Abre `http://127.0.0.1:5000/` en el navegador. Usa esa dirección para que Flask atienda también `/api/pila`; abrir `templates/index.html` directamente o mediante Live Server provoca respuestas HTML donde JavaScript espera JSON.

En PowerShell, si la activación del entorno está restringida, usa `.venv\Scripts\python.exe -m pip install -r requirements.txt` y luego `.venv\Scripts\python.exe app.py`.

## Operaciones

- **Palabras:** agrega texto al tope (máximo 40 caracteres).
- **Imágenes:** acepta JPG, PNG, WEBP y GIF de hasta 5 MB. Se muestra una vista previa antes de apilar.
- **Cámara:** en el modo Imágenes puedes abrir la cámara, tomar una foto, revisarla y apilarla sin elegir un archivo. El navegador pedirá permiso; funciona desde `localhost` o HTTPS.
- **Tamaño de la pila:** empieza en 8 elementos y puede cambiarse entre 1 y 20 por separado para palabras e imágenes. No se puede reducir por debajo de la cantidad actual.
- **Desapilar:** retira el elemento del tope de la opción actual.
- **Vaciar pila:** elimina los elementos de la opción actual. Las imágenes retiradas también se eliminan del almacenamiento local.
- **Cambiar opción:** vuelve a los dos paneles; la otra pila conserva su contenido.
- **Reordenar:** arrastra el icono a la derecha de un elemento y suéltalo sobre otra posición. También puedes enfocar el icono y usar las flechas arriba y abajo.
- **Código Python:** muestra las llamadas `append(...)`, la cantidad actual y el tope según los elementos visibles.

Las imágenes se guardan en `instance/uploads/`, un directorio excluido de Git. Los GIF se representan mediante su primer fotograma.

La sesión del navegador conserva la pila mientras Flask use la misma clave secreta. Para un despliegue real, configura `FLASK_SECRET_KEY` con un secreto aleatorio y no ejecutes Flask con `debug=True`.
