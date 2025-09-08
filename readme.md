# Probador Automatizado para la API del Restaurante

Sigue estos pasos para verificar si tu API cumple con los requisitos de la Parte 1.

### Paso 1: Prepara tu Entorno

Abre una terminal en la carpeta donde descomprimiste estos archivos. Es una buena práctica crear un entorno virtual para instalar las dependencias.

```bash
# Crea el entorno virtual (solo la primera vez)
python3 -m venv venv
py -m venv venv 

# Actívalo
# En macOS/Linux:
source venv/bin/activate
# En Windows:
.\venv\Scripts\activate


#Instala dependencias
pip install -r requirements.txt

#Vuelve a la terminal donde tienes el probador activado y ejecuta pytest. Reemplaza la URL de ejemplo con la URL de tu API.
pytest --api-url=[http://127.0.0.1:8000](http://127.0.0.1:8000)

#Analiza los Resultados
pytest te mostrará un resumen de las pruebas. Si todo está en verde (passed), ¡felicidades! Si ves errores en rojo (FAILED), el reporte te indicará qué prueba falló y por qué, para que puedas corregir tu código.

