# 🤖 Probador Automatizado - API de Restaurante

Este proyecto contiene un conjunto de pruebas automáticas para validar que tu API del restaurante cumpla con todos los requisitos de la **Parte 1** del Trabajo Práctico.

Usar este probador te permitirá verificar tu código de forma rápida y autónoma, asegurando que cumples con las validaciones y flujos definidos en la especificación OpenAPI.

---

## 📋 Requisitos Previos

-   Tener **Python** instalado en tu sistema (versión 3.8 o superior).
-   Tener acceso a la **terminal** o línea de comandos de tu sistema.

---

## ⚙️ Paso 1: Configuración Inicial

Sigue estos pasos la **primera vez** que uses el probador para configurar tu entorno de trabajo.

1.  **Abre una terminal** en la carpeta donde descomprimiste estos archivos.
2.  **Crea un entorno virtual**. Esto aísla las librerías del proyecto.
    ```bash
    # Elige el comando que funcione en tu sistema
    python3 -m venv venv
    # O si usas Windows:
    py -m venv venv
    ```
3.  **Activa el entorno virtual**. Debes hacer esto cada vez que abras una nueva terminal para trabajar en el proyecto.
    ```bash
    # En macOS o Linux:
    source venv/bin/activate

    # En Windows (CMD o PowerShell):
    .\venv\Scripts\activate
    ```
    *Verás `(venv)` al principio de la línea de tu terminal si se activó correctamente.*
4.  **Instala las dependencias** necesarias para que el probador funcione.
    ```bash
    pip install -r requirements.txt
    ```

---

## ▶️ Paso 2: Cómo Ejecutar las Pruebas

Una vez que tu entorno esté configurado, sigue estos pasos cada vez que quieras probar tu API.

1.  **Inicia tu API**. En una terminal separada, ejecuta tu proyecto del restaurante. Asegúrate de que esté funcionando y anota la URL base (por ejemplo, `http://127.0.0.1:8000`).
2.  **Ejecuta el probador**. Vuelve a la terminal donde tienes el entorno `(venv)` activado y ejecuta el siguiente comando, **reemplazando la URL de ejemplo** con la de tu API.
    ```bash
    pytest --api-url=http://127.0.0.1:8000                 
    ```

IMPORTANTE: Debes buscar la URL de http (no https) , y es importante comentar la linea de  app.UseHttpsRedirection(); en tu program.cs.

---

## 📊 Paso 3: Entendiendo los Resultados

Al finalizar, `pytest` te mostrará un resumen con los resultados de todas las pruebas.

-   ✅ **`PASSED` (en verde)**: ¡Excelente! Significa que tu API respondió exactamente como se esperaba para esa prueba.
-   ❌ **`FAILED` (en rojo)**: Indica que tu API no cumplió con lo esperado. El reporte te dará detalles sobre qué prueba falló y por qué, comparando el valor que se obtuvo con el que se esperaba.
-   🔶 **`ERROR` (en amarillo)**: Generalmente indica un problema en la prueba misma o que tu API se cayó y no pudo responder.

Usa los mensajes de error para depurar tu código, corrige los problemas y vuelve a ejecutar las pruebas hasta que todas pasen.
