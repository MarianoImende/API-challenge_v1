# API-challenge
API para automation challenge

# Resumen de la API de Wallet Redlink

La API Wallet Redlink es un servicio que brinda a los usuarios la capacidad de gestionar sus cuentas bancarias, realizar transacciones y acceder de forma segura a su información financiera. Esta API se ha diseñado con un enfoque en la seguridad y la eficiencia.

**Nota: La API Wallet Redlink se encuentra en proceso de construcción y desarrollo, por lo que la información proporcionada puede estar sujeta a cambios y actualizaciones.**

## Funcionalidades Principales:

### Autenticación y Sesión:

La API admite la autenticación de usuarios mediante un mecanismo basado en tokens JWT (JSON Web Tokens). Para solicitar un token de acceso, los usuarios deben proporcionar las siguientes credenciales: usuario: Bhikkhu, contraseña: Redlink*9.

Los usuarios pueden obtener un token de acceso a través de la ruta `redlink/wallet/sesion`. Este token es necesario para acceder a las rutas protegidas.

Las rutas protegidas requieren que los usuarios envíen su token de acceso para su validación. Si el token es válido y no ha expirado, se permite el acceso a la funcionalidad protegida. En caso contrario, la API devolverá un mensaje de error con un código de estado 401.

### Cuentas y Tarjetas:

Los usuarios pueden acceder a información sobre sus cuentas bancarias y tarjetas a través de rutas como `/redlink/wallet/cuentas`.

La API realiza validaciones para asegurarse de que los datos proporcionados por el usuario sean correctos. Por ejemplo, verifica que el campo "numero" sea una cadena de dígitos, que no esté vacío ni sea nulo, y que sea del tipo cadena (String). En caso de no cumplir con estas condiciones, se generará una excepción HTTP con un código de estado 400 (Solicitud incorrecta).

### Saldo y Últimos Movimientos:

Los usuarios pueden consultar el saldo de sus cuentas y los últimos movimientos en sus cuentas a través de las rutas `/redlink/wallet/saldo` y `/redlink/wallet/ultmovimientos`.

La API valida los números de cuenta para asegurarse de que sean cadenas de dígitos válidas y de que no estén vacíos ni sean nulos. Asimismo, se verifica que las fechas "fecha_desde" y "fecha_hasta" cumplan con un formato específico (por ejemplo, AAAAMMDD). Si no se cumplen estas condiciones, se generará una excepción HTTP con un código de estado 400 y un mensaje de "Datos inválidos".Además, siempre la fecha_desde debe ser menor a fecha_hasta.

### Cerrar Sesión:

Los usuarios tienen la opción de cerrar sesión a través de la ruta `/billetera/redlink/logout`. Esta acción invalida su token de acceso y les impide acceder a las rutas protegidas.Si se intenta utilizar o reutilizar un token invalido se devuelve un error “HTTP 401 Token Invalido”. 

### Seguridad:

La API utiliza tokens JWT para autenticar a los usuarios y garantizar la seguridad de las rutas protegidas. Los tokens de acceso tienen un tiempo de expiración de 30 minutos para aumentar la seguridad.

### Documentación:

La API se documenta de forma automática y se integra con Swagger OpenAPI para proporcionar una guía detallada de todas las rutas y parámetros disponibles. Se incluyen ejemplos para facilitar la comprensión y prueba de la API.

**Nota: Puedes acceder a la documentación de la API en el siguiente enlace:**
[Documentación de la API Wallet Redlink](https://api-challenge-wallet.onrender.com/docs)

