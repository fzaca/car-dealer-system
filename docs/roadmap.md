# Car Dealership Management System

## Descripción del Proyecto
Este proyecto es un sistema de gestión para una concesionaria de autos desarrollado utilizando Django. El sistema permite la gestión de autos, marcas, modelos, clientes, categorías, comentarios y usuarios con diferentes roles (staff y no staff).

## Fases del Proyecto

### Fase 1: Configuración Inicial
1. **Configuración del entorno de desarrollo**
   - Configurar el entorno virtual y las dependencias necesarias.
   - Configurar el repositorio de GitHub.

2. **Estructura básica del proyecto**
   - Crear la estructura del proyecto Django.
   - Configurar el archivo `settings.py` y crear las aplicaciones básicas.

### Fase 2: Modelos de Base de Datos
1. **Definir modelos principales**
   - Crear los modelos para Autos, Marcas, Modelos de autos, Clientes, Categorías, Comentarios, y Usuarios (con roles).
   - Definir las relaciones entre los modelos.

2. **Migraciones**
   - Crear y aplicar migraciones para los modelos definidos.

### Fase 3: Autenticación y Roles de Usuarios
1. **Autenticación de Usuarios**
   - Implementar formularios de registro e inicio de sesión.
   - Configurar vistas y URLs para la autenticación.

2. **Roles de Usuarios**
   - Configurar roles de usuarios en el modelo de Usuario.
   - Implementar permisos y restricciones de acceso basados en roles.

### Fase 4: Funcionalidades CRUD y Carga de Imágenes
1. **Autos y Marcas**
   - Implementar vistas para crear, leer, actualizar y eliminar autos y marcas.
   - Implementar la carga de imágenes para los autos.

2. **Modelos de Autos y Categorías**
   - Implementar vistas CRUD para modelos de autos y categorías.

### Fase 5: Comentarios y Restricciones de Acceso
1. **Comentarios**
   - Implementar vistas y formularios para que los usuarios no staff puedan añadir, editar y eliminar sus propios comentarios.
   - Implementar funcionalidad para que los usuarios staff puedan ver y eliminar comentarios.

2. **Restricciones de Acceso**
   - Configurar restricciones de acceso para las vistas utilizando `LoginRequiredMixin` y permisos personalizados.

### Fase 6: Interfaz de Usuario y Experiencia de Usuario
1. **Templates y Estilo**
   - Diseñar y desarrollar templates para las vistas principales del sistema.
   - Implementar estilos CSS para mejorar la interfaz de usuario.

2. **Navegación y Usabilidad**
   - Mejorar la navegación del sitio para que sea intuitiva y fácil de usar.
   - Asegurar que las funcionalidades clave estén fácilmente accesibles.

### Fase 7: Validación y Pruebas
1. **Validación de Datos**
   - Asegurar la correcta validación de datos en los formularios.

2. **Pruebas**
   - Escribir pruebas unitarias y de integración para las funcionalidades clave.
   - Realizar pruebas manuales para asegurarse de que el sistema funciona como se espera.

### Fase 8: Documentación y Entrega
1. **Documentación del Proyecto**
   - Escribir un README.md detallado con instrucciones de instalación y configuración.
   - Incluir una descripción del proyecto y capturas de pantalla (opcional).

2. **Entrega Final**
   - Asegurarse de que el proyecto esté bien documentado y funcional.
   - Subir el proyecto completo al repositorio de GitHub.
