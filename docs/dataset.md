## Dataset (Temp file)

* Web: https://deepvisualmarketing.github.io/
* Manual: https://deepvisualmarketing.github.io/site-assets/DVM_user_manual.pdf


### tablas
Basic table: car attributes such as model name, model ID and brand name.
Sales table: ten years car sales data in UK/GB.
Price table: entry-level (i.e. the cheapest trim price) new car prices across years.
Trim table: trim attributes like the selling price (trim level), engine type and engine size.
Ad table: more than 0.25 million used car advertisements.
Image table: car images attributes like colour and viewpoint.


### Modelos redefinidos para este dataset

#### Marca (Brand)
* id (PrimaryKey)
* name (CharField, unique=True)

#### Modelo de Auto (CarModel)
* id (PrimaryKey)
* brand (ForeignKey to Brand)
* name (CharField)

#### Versión del Modelo (Trim)
* id (PrimaryKey)
* car_model (ForeignKey to CarModel)
* name (CharField)
* year (PositiveIntegerField)
* price (DecimalField)
* fuel_type (CharField)
* engine_size (DecimalField)

#### Carro (Car)
* id (PrimaryKey)
* car_model (ForeignKey to CarModel)
* trim (ForeignKey to Trim)
* year (PositiveIntegerField)
* price (DecimalField)
* image (ImageField, upload_to='cars/')
* color (CharField)
* registration_year (PositiveIntegerField)
* mileage (PositiveIntegerField)

#### Venta (Sale)
* id (PrimaryKey)
* car (ForeignKey to Car)
* sale_date (DateTimeField, auto_now_add=True)
* price (DecimalField)

#### Cliente (Customer)
* id (PrimaryKey)
* user (ForeignKey to CustomUser)
* phone (CharField, null=True)
* address (TextField, null=True)

#### Comentario (Comment)
* id (PrimaryKey)
* car (ForeignKey to Car)
* user (ForeignKey to CustomUser)
* comment (TextField)
* date (DateTimeField, auto_now_add=True)

#### Usuario Personalizado (CustomUser)
* id (PrimaryKey)
* Inherits from AbstractUser
* is_staff (BooleanField)
* is_customer (BooleanField)
* is_employee (BooleanField, default=False)


### Metadata 

#### Descripción del Diagrama
CUSTOM_USER: Representa a los usuarios del sistema, ya sean clientes, empleados o personal administrativo.
CUSTOMER: Representa a los clientes del concesionario.
EMPLOYEE: Representa a los empleados del concesionario.
BRAND: Representa las marcas de autos.
CAR_MODEL: Representa los modelos de autos.
TRIM: Representa las versiones específicas de los modelos de autos.
CAR: Representa los autos disponibles en el concesionario.
SALE: Representa las ventas realizadas en el concesionario.
COMMENT: Representa los comentarios hechos por los usuarios sobre los autos.

#### Relaciones
CUSTOMER -> CUSTOM_USER: Un cliente pertenece a un usuario personalizado.
EMPLOYEE -> CUSTOM_USER: Un empleado pertenece a un usuario personalizado.
CAR_MODEL -> BRAND: Un modelo de auto pertenece a una marca.
TRIM -> CAR_MODEL: Una versión de un modelo de auto pertenece a un modelo de auto.
CAR -> CAR_MODEL: Un auto pertenece a un modelo de auto.
CAR -> TRIM: Un auto tiene una versión específica.
SALE -> CAR: Una venta incluye un auto.
COMMENT -> CAR: Un comentario está relacionado con un auto.
COMMENT -> CUSTOM_USER: Un comentario es hecho por un usuario personalizado.