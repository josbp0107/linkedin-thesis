# LinkedIn Thesis

Este proyecto está basado en el desarrollo de una herramienta para la extracción, almacenamiento y procesamiento de datos de los egresados de la Corporacion Universitaria del Caribe CECAR del programa de Ingeniera de Sistemas, donde se realiza un scraping o raspado de las cuentas de estos egresado para contar con un monitoreo de su evolución educativa y laboral.

<blockquote>
<p>Este proyecto es desarrollado para la Coporacion Universitaria del Caribe CECAR como Proyecto de grado</p>
</blockquote>

## Tecnologias
1. Python.
2. Selenium.
3. Web Driver.

### Funcionalidades de la aplicación
1. Extraer datos de los perfiles de egresados de la Corporacion Universitaria del Caribe desde LinkedIn.


### Clona el repositorio

`git clone https://github.com/josbp0107/linkedin-thesis.git`

`cd linkedin-thesis`

### Instalar modulos en un entorno virtual
Linux & Mac

`python3 -m venv venv`

`source venv/bin/activate`

`pip3 install -r requirements.txt`

Windows

`py -m venv venv`

`venv\Scrips\activate`

`pip install -r requirements.txt`


### Archivos requeridos

Es necesario agregar un nuevo archivo el cual contendrá las credenciales del usuario de LinkedIn.

Es recomendable nombrar este archivo como **account.txt**

### ChromeDriver

Debes descargar el driver de Chrome para poder realizar la automatizacion y el respectivo scraping en la pagina de LinkedIn.

1. https://chromedriver.chromium.org/downloads
2. Luego de haber descargado el driver, debes crear una carpeta en la raiz con el nombre drivers
3. Y finalmente, dentro de esta carpeta debes agrega el driver.

### Ejecutar proyecto 

Linux & Mac

`python3 main.py`

Windows

`py main.py`
