# 🏥 - SaludHoy API

API REST para la gestión de citas médicas, desarrollada por FastAPI y MongoDB.

## 💻 - Stack tecnológico

- **Python 3.12**
- **FastAPI** framework web.
- **MongoDB** - Base de datos NoSQL.
- **Motor** - Driver asíncrono para MongoDB.
- **JWT** - Autenticación con tokens.
- **Passlib / Bcrypt** - Cifrado de contraseñas.
- **Pydantic** - Validación de datos.
- **Python-dotenv** - Gestión de variables de entorno.

## 🎯 - Requisitos previos

- Python 3.12+
- MongoDB corriendo localmente o una URL de MongoDB Atlas.

## 🔧 - Instalación y ejecución local

1. Clona el repositorio
```bash
    git clone https://github.com/AngelSoulZ99/saludhoy-api.git
    cd saludhoy-api
```

2. Crea y activa el entorno virtual
```bash
    python -m venv venv

    # Windows
    venv/Scripts/activate
        # En caso de tener conflictos de permisos (No se puede cargar el archivo... porque la ejecución de scripts está deshabilitada en este sistema)
        # Puedes ejecutar el siguiente permiso como administrador en Powershell.
        Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

    # Mac / Linux
    source venv/bin/activate
```

3. Instala las dependencias
```bash
    pip install -r requirements.txt
```

4. Crea el archivo `.env` en la raíz del proyecto.
```env
    MONGO_URI=mongodb://localhost:27017
    DB_NAME=saludhoy
    SECRET_KEY=tu_clave_secreta
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. Corre el servidor.
```bash
    uvicorn app.main:app --reload
```

6. Accede a la documentación automática en `http://localhost:8000/docs`

## 🗂️ - Estructura del proyecto
```
saludhoy-api/
|--app/
|  |--main.py #Entrada de la aplicación
|  |--config.py #Variables de entorno
|  |--database.py #Conexión a MongoDB
|  |--core/ #Seguridad y dependencias (JWT, roles)
|  |--models/ #Esquemas Pydantic
|  |--routers/ #Endpoint organizados por dominio
|  |--services/ #Lógica de negocio
|--.env #Variables de entorno (No incluida en GIT)
|--.gitignore
|--requirements.txt
|--README.md
...
```

## 🚹 - Roles del sistema

| Rol | Permisos |
|---|---|
| Administrador | Acceso total: Gestión de médicos, pacientes, citas y reportes |
| Médico | Consulta de pacientes, agenda de citas e historia clínica |
| Paciente | Solicitud y consulta de sus propias citas |

## 🔚 - Endpoints

> Documentación completa disponible en `/docs` una vez el servidor esté corriendo.

*En construcción - se irán añadiendo conforme avance el desarrollo del proyecto.*

## 👷 - Estado del proyecto

🚧 En desarrollo activo - `v0.1.0`

## 🧑‍💻 - Autor

Brayan Stiven Velasquez Riaño