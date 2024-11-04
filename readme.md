# Calculadora Básica

¡Bienvenido a la **Calculadora Básica**! Este es un proyecto desarrollado como parte de un servicio social con el objetivo de proporcionar una herramienta accesible y útil para estudiantes, especialmente aquellos con discapacidad visual. La calculadora es completamente accesible con lectores de pantalla y está diseñada para ser sencilla y fácil de usar.

## Descripción

La Calculadora Básica es una aplicación escrita en Python utilizando la biblioteca gráfica `wxPython`. Ofrece una variedad de operaciones matemáticas y conversiones de unidades, incluyendo:

- **Aritmética básica**: suma, resta, multiplicación, división, raíces, potencias, logaritmos y evaluaciones de expresiones matemáticas.
- **Conversión de unidades**: temperatura, longitud, capacidad, tiempo, velocidad, ángulo, frecuencia e información.
- **Funciones trigonométricas**: seno, coseno, tangente y sus inversas.
- **Cambio de bases numéricas**: conversión entre binario, octal, decimal y hexadecimal.
- **Cálculos geométricos**: áreas y perímetros de círculos y triángulos.

## Contenido del Repositorio

- `calc.py`: Código fuente principal de la aplicación que contiene la interfaz gráfica y la lógica de interacción con el usuario.
- `operaciones.py`: Módulo que contiene las clases y métodos para realizar las operaciones matemáticas y conversiones.
- update.py: Archivo python donde se tiene la lógica de negocio del actualizador.
- update.exe: Archivo update.py compilado.
- `documentacion.html`: Archivo HTML con la documentación de usuario y desarrollador.
- `README.md`: Este archivo con información sobre el proyecto.

## Requisitos

- **Python 3.7**: Asegúrate de tener instalado Python 3.7 o superior  en tu sistema.
- **wxPython**: Biblioteca para la interfaz gráfica.
- **SymPy**: Biblioteca para operaciones matemáticas simbólicas.

Puedes instalar las dependencias ejecutando:

```bash
pip install wxPython sympy
```

## Instrucciones de Uso

1. **Ejecución directa**: Puedes ejecutar la calculadora directamente desde el código fuente.

   ```bash
   python calc.py
   ```

2. **Interfaz de usuario**: Al iniciar la aplicación, encontrarás botones para acceder a las distintas operaciones. La aplicación es accesible mediante lectores de pantalla.

3. **Documentación**: Hay un botón llamado **"Leer Documentación"** que abrirá un archivo HTML con instrucciones detalladas para el usuario y desarrolladores.

## Compilación a Ejecutable

Si deseas distribuir la aplicación sin necesidad de que los usuarios tengan Python instalado, puedes compilarla a un ejecutable utilizando `PyInstaller`.

### Comando de Compilación

Ejecuta el siguiente comando en la terminal desde el directorio donde se encuentra `calc.py`:

```bash
pyinstaller --windowed --onedir --name basic_calculathor1.0 calc.py --add-data "documentacion.html;." --add-binary "update.exe;." --hidden-import=packaging

```

**Nota**: Este comando es para sistemas Windows. Si estás en macOS o Linux, reemplaza `;` por `:` en la opción `--add-data`:

```bash
pyinstaller --windowed --onedir --name Calculadora0.3 calc.py --add-data "documentacion.html;." --hidden-import packaging

```

### Explicación del Comando

- `--windowed`: Crea una aplicación GUI sin consola.
- `--onedir`: Crea una carpeta con todos los archivos necesarios.
- `--name Calculadora0.2`: Nombra el ejecutable como "Calculadora0.2".
- `calc.py`: Archivo principal de la aplicación.
- `--add-data "documentacion.html;."`: Incluye el archivo `documentacion.html` en el directorio raíz del ejecutable.

## Para Desarrolladores

### Estructura del Proyecto

- **`calc.py`**: Contiene la interfaz gráfica y maneja la interacción con el usuario. Define las clases para los diferentes diálogos y ventanas de la aplicación.
- **`operaciones.py`**: Contiene las clases y métodos que implementan la lógica de las operaciones matemáticas y conversiones.

### Añadiendo Nuevas Operaciones

Para extender la funcionalidad de la calculadora, sigue estos pasos:

1. **Agregar la lógica en `operaciones.py`**:

   - Crea una nueva clase o añade un método a una clase existente para implementar la nueva operación.
   - Asegúrate de manejar excepciones y validar entradas si es necesario.

2. **Actualizar la interfaz en `calc.py`**:

   - Añade la nueva operación a la lista correspondiente en los métodos que muestran categorías u operaciones, como `mostrar_categorias` o `operaciones_aritmeticas`.
   - Si es necesario, crea una nueva clase de diálogo siguiendo el formato de las existentes (`DialogoAritmetica`, `DialogoConversion`, etc.).
   - En el diálogo, implementa los campos de entrada y botones necesarios, y enlaza los eventos a los métodos adecuados.

3. **Enlazar la interfaz con la lógica**:

   - En el método que maneja el evento de cálculo, llama al método correspondiente en `operaciones.py` con los parámetros adecuados.

### Accesibilidad

Este proyecto pone un énfasis especial en la accesibilidad para usuarios con discapacidad visual. Se recomienda seguir buenas prácticas de accesibilidad al añadir nuevas funcionalidades:

- **Etiquetas claras**: Asegúrate de que todos los controles (botones, campos de entrada, etc.) tengan etiquetas descriptivas.
- **Navegación con teclado**: Verifica que la aplicación pueda ser navegada completamente usando el teclado.
- **Mensajes de error y ayuda**: Proporciona mensajes claros y concisos que puedan ser leídos por lectores de pantalla.

## Contribución

Si deseas contribuir al proyecto, puedes hacerlo de la siguiente manera:

1. **Fork del repositorio**: Crea un fork de este repositorio en tu cuenta de GitHub.
2. **Clona el repositorio**: Clona el fork en tu máquina local.
3. **Crea una rama**: Crea una nueva rama para tu funcionalidad o corrección.
4. **Realiza cambios**: Implementa tus mejoras siguiendo las directrices mencionadas.
5. **Realiza un pull request**: Envía tus cambios a este repositorio mediante un pull request.

## Licencia y Uso

Este proyecto es de código abierto y está liberado para su uso por parte de estudiantes con discapacidad visual que puedan encontrarlo útil. Aunque fue desarrollado como parte de un proyecto de servicio social, se anima a otros a utilizarlo, modificarlo y mejorarlo para beneficio de la comunidad.

## Contacto

Para cualquier duda, sugerencia o comentario, puedes contactarme:

- **Nombre**: Ángel Alcántar
- **Email**: rayoalcantar@gmail.com

¡Gracias por tu interés en este proyecto y por contribuir a hacerlo más accesible y útil para todos!