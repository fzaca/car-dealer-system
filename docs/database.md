### Esquema

#### Car (Auto)
- `id` (PrimaryKey)
- `brand_id` (ForeignKey to Brand)
- `model_id` (ForeignKey to CarModel)
- `year` (PositiveIntegerField)
- `price` (DecimalField)
- `image` (ImageField)
- `category_id` (ForeignKey to Category)

#### Brand (Marca)
- `id` (PrimaryKey)
- `name` (CharField, unique=True)

#### CarModel (Modelo de Auto)
- `id` (PrimaryKey)
- `brand_id` (ForeignKey to Brand)
- `name` (CharField)

#### Customer (Cliente)
- `id` (PrimaryKey)
- `user_id` (ForeignKey to CustomUser)
- `phone` (CharField, null=True) // Added phone field
- `address` (TextField, null=True) // Added address field

#### Category (Categoría)
- `id` (PrimaryKey)
- `name` (CharField, unique=True)

#### Comment (Comentario)
- `id` (PrimaryKey)
- `car_id` (ForeignKey to Car)
- `user_id` (ForeignKey to CustomUser)
- `comment` (TextField)
- `date` (DateTimeField, auto_now_add=True)

#### CustomUser (Usuario con roles de staff y no staff)
- `id` (PrimaryKey)
- Inherits from AbstractUser
- `is_staff` (BooleanField)
- `is_customer` (BooleanField)
- `is_salesperson` (BooleanField, default=False) // New field to distinguish salespeople

#### Sale (Venta)
- `id` (PrimaryKey)
- `car_id` (ForeignKey to Car)
- `customer_id` (ForeignKey to Customer)
- `sale_date` (DateTimeField, auto_now_add=True)
- `price` (DecimalField)
- `salesperson_id` (ForeignKey to Employee, null=True)

#### Service (Servicio realizado a un auto)
- `id` (PrimaryKey)
- `car_id` (ForeignKey to Car)
- `service_date` (DateTimeField, auto_now_add=True)
- `description` (TextField)
- `cost` (DecimalField)
- `supplier_id` (ForeignKey to Supplier, null=True) // Added to track who provided the service

#### Supplier (Proveedor de autos o partes)
- `id` (PrimaryKey)
- `name` (CharField)
- `contact_info` (TextField)
- `address` (TextField)

#### Invoice (Factura)
- `id` (PrimaryKey)
- `sale_id` (ForeignKey to Sale)
- `amount` (DecimalField)
- `issue_date` (DateTimeField, auto_now_add=True)
- `due_date` (DateTimeField)

#### Payment (Representa un pago realizado por una factura)
- `id` (PrimaryKey)
- `invoice_id` (ForeignKey to Invoice)
- `amount` (DecimalField)
- `payment_date` (DateTimeField, auto_now_add=True)
- `payment_method` (CharField)

#### Employee (Representa un empleado de la concesionaria)
- `id` (PrimaryKey)
- `user_id` (ForeignKey to CustomUser, null=True)
- `name` (CharField)
- `position` (CharField)
- `hire_date` (DateTimeField)
- `salary` (DecimalField)
- `department` (CharField, null=True) // Added department field

#### Warranty (Garantía)
- `id` (PrimaryKey)
- `car_id` (ForeignKey to Car)
- `warranty_period` (PositiveIntegerField, in months)
- `start_date` (DateTimeField)
- `end_date` (DateTimeField)
- `details` (TextField)

### Tablas opcionales

#### TestDrive (Prueba de Manejo)
- `id` (PrimaryKey)
- `car_id` (ForeignKey to Car)
- `customer_id` (ForeignKey to Customer)
- `employee_id` (ForeignKey to Employee, null=True)
- `date` (DateTimeField, auto_now_add=True)
- `notes` (TextField, null=True)

#### Part (Pieza)
- `id` (PrimaryKey)
- `name` (CharField)
- `description` (TextField, null=True)
- `supplier_id` (ForeignKey to Supplier)
- `price` (DecimalField)

#### PartOrder (Pedido de Piezas)
- `id` (PrimaryKey)
- `part_id` (ForeignKey to Part)
- `quantity` (IntegerField)
- `order_date` (DateTimeField, auto_now_add=True)
- `supplier_id` (ForeignKey to Supplier)

### Diagrama
https://www.blocksandarrows.com/editor/K7Dx07CsGG3ONbeg