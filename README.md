# Car Dealer System

## Instalación y Configuración

1. Clona el repositorio:
```sh
git clone https://github.com/fzaca/car-dealer-system.git
cd car-dealer-system
```

2. Crea un entorno virtual e instala las dependencias:
```sh
python3.12 -m venv env
source env/bin/activate
pip install -r requirements/local.txt
```
> [!NOTE]
>
> Si no tienes Python 3.12 instalado, puedes instalarlo en Linux con los siguientes comandos:
> ```sh
> sudo apt update
> sudo apt install -y python3.12 python3.12-venv python3.12-dev
> ```

3. Instala las dependencias de Node.js y construye el CSS de Tailwind:
```sh
npm install
npm run build:css
```

4. Configura las variables de entorno en un archivo `local.env`.
```sh
cp .env.example environments/local.env
```
Asegúrate de editar el archivo `.env` con los valores adecuados para tu entorno local.

5. Ejecuta las migraciones y arranca el servidor de desarrollo:
```sh
python manage.py migrate
python manage.py runserver
```

## Configuración de entornos

Para seleccionar el entorno adecuado, establece la variable de entorno `ENV` antes de ejecutar las tareas de Django.

Ejemplo para entorno local:
```sh
export ENV=local
```

Ejemplo para entorno remoto:
```sh
export ENV=remote
```

## Cargar Datos del Dataset
* Dataset: [DVM-CAR Dataset](https://deepvisualmarketing.github.io/
)
Para cargar los datos del dataset en la base de datos, sigue estos pasos:
1. Coloca los archivos CSV del dataset en la ruta correcta. Asegúrate de tener los archivos:
    * `brands.csv`
    * `car_models.csv`
    * `cars.csv`
2. Ejecute los comandos de carga de datos en orden:
```sh
python manage.py load_car_images
python manage.py load_car_data
python manage.py load_sales_data
```

## Depuración
### Debugging con `ipdb`
Para depurar utilizando `ipdb`, añade un breakpoint en tu código con `import ipdb; ipdb.set_trace()`.

> [!NOTE]
>
> Si lo corres en docker abre una terminal nueva, o corriendo el compose con `-d`(detached) adjunta al contenedor de la API:
> ```sh
> docker attach container
> ```

## Linting y Formateo
### Instalación de `pre-commit`
Para instalar `pre-commit` y configurarlo en tu proyecto, sigue estos pasos:
1. Instala `pre-commit` utilizando pip:
```sh
pip install pre-commit
```
2. Instala los hooks de pre-commit:
```sh
pre-commit install
```
3. Ejecuta los hooks manualmente para verificar todos los archivos:
```sh
pre-commit run --all-files
```

### Uso Manual de `ruff`
Para utilizar `ruff` manualmente y asegurarte de que tu código cumple con los estándares, sigue estos pasos:
1. Instala `ruff` utilizando pip (si no lo has hecho ya):
```sh
pip install ruff
```
2. Ejecuta ruff en tu código para verificar:
```sh
ruff path/to/your/code
```
3. Para corregir automáticamente los problemas detectados, puedes usar la opción --fix:
```sh
ruff path/to/your/code --fix
```
