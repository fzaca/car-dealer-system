## users

Descripción: Gestión de usuarios y autenticación.
Modelos: User (extensión del modelo de usuario de Django, con roles de staff y no staff).
Funcionalidades: Registro, inicio de sesión, roles y permisos.

## cars

Descripción: Gestión de autos, marcas y modelos de autos.
Modelos: Car, Brand, CarModel.
Funcionalidades: CRUD de autos, marcas y modelos, carga de imágenes.

## customers

Descripción: Gestión de clientes.
Modelos: Customer.
Funcionalidades: CRUD de clientes.

## categories

Descripción: Gestión de categorías de autos.
Modelos: Category.
Funcionalidades: CRUD de categorías.

## comments

Descripción: Gestión de comentarios de los usuarios sobre los autos.
Modelos: Comment.
Funcionalidades: CRUD de comentarios, con restricciones basadas en roles.

## media

Descripción: Gestión de imágenes y archivos subidos.
Modelos: Ninguno específico, pero configuración de rutas y almacenamiento de media.
