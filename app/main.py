"""
    ------------------------------------------------------------------------------API-----------------------------------------------------------------------------------
    Qué es una API (Application Programming Interface): es un conjunto de reglas y herramientas que permite que un programa se comunique con otro.
    La API recibe una petición, la traduce para el sistema, y devuelve una respuesta. Es como cuando vas a un restaurante y le hace un pedido al mesero (la API), y él lleva la orden a la cocina (el sistema interno) y luego devuelve el plato listo. Las API manejan endpoints que aceptan solicitudes (GET, POST, PUT, DELETE) y devuelven datos en formatos como JSON.

    Para ser más claro, una API es como un puente entre el frontend (lo que el usuario ve en el navegador) y el backend (el servidor donde están los datos y la lógica).

    Estructura de una API: se organiza en varias partes claras:
    mi-api
    |---- app/
            |---- main.py
            |---- api/
            |---- core/
            |---- database/
            |---- models/
            |---- schemas/
            |---- services/
    |---- entorno/
    |---- test/

    ---------------------------------------------------------------------------ENDPOINTS--------------------------------------------------------------------------------
    Qué son los endpoints: son como una puerta de entrada, es decir, es una URL específica dentro del servidor, está asociada a un método HTTP (GET, POST, PUT, DELETE) que recibe una petición de un usuario y responde con datos (normalmente JSON).

    GET -> lee o trae datos del servidor. Ejemplo: obtener la lista de usuarios.
    POST -> crea un nuevo recurso en el servidor. Ejemplo: agregar un nuevo usuario.
    PUT -> actualiza completamente un recurso existente. Ejemplo: cambiar los datos de un usuario por completo.
    DELETE -> borra un recurso existente. Ejemplo: eliminar un usuario por su id.

    -----------------------------------------------------------------------------CORE-----------------------------------------------------------------------------------
    Qué es el core: es donde se coloca la configuración y la lógica central de la aplicación. No son endpoints, ni modelos, ni esquemas, sino las cosas fundamentales que necesita la API para funcionar. Se puede encontrar archivos como:

    config.py -> variables de configuración (puerto, debug, claves secretas, etc.).
    security.py -> autenticación, manejo de contraseñas, JWT, etc.
    settings.py -> parámetros globales de la aplicación.
    loggins.py -> configuración de logs.

    ---------------------------------------------------------------------------DATABASE---------------------------------------------------------------------------------
    Qué es database: suele ser un archivo o una carpeta que se encarga de configurar la conexión a la base de datos y preparar las herramientas necesarias para interactuar con ella. Suele contener la conexión a la base datos (URL, motor, credenciales), creación de engine (motor de conexión con SQLAlchemy), sesiones (SessionLocal) para abrir / cerrar transacciones con la base de datos y declarative Base (la "base" de los modelos que definen las tablas).

    ----------------------------------------------------------------------------MODELS----------------------------------------------------------------------------------
    Qué son models: son la representaciones de los datos en la base de datos, mientras que los schemas definen como deberían lucir los datos que entran y salen de la API, los models definen cómo se almacenan realmente en la base de datos, normalmente se crean usando un ORM (Object-Relational Mapping), como SQLAlchemy, que permite trabajar con bases de datos usando objetos de Python en lugar de escribir SQL puro.

    ----------------------------------------------------------------------------SCHEMAS---------------------------------------------------------------------------------
    Qué son los schemas: son un modelo de datos que define cómo deberían lucir los datos que entran o salen de la API. Permiten validar datos que el usuario envia, estandarizar la forma de los datos que la API devuelve y evitar errores y asegurarse de que todos los campos tengan el tipo correcto.

    ---------------------------------------------------------------------------SERVICES---------------------------------------------------------------------------------
    Qué son los services: son la lógica de negocio de la aplicación, es decir, es el nivel intermedio donde se ponen las reglas de negocio, es la lógica que no debería estar ni en los endpoints ni en el acceso crudo a datos.

    -----------------------------------------------------------------------------TESTS----------------------------------------------------------------------------------
    Qué son los tests (unitarios, integración, endpoints): es donde se guardan los tests automáticos del código, es decir, contiene los archivos que prueban que la API funciona como debería, cada archivo comienza con test_ y dentro cada función tambien comienza con test_ y se ejecutan con la librería pytest. Se realizan pruebas para:

    Endpoints -> que devuelvan lo esperado en (GET, POST, PUT, DELETE).
    Validaciones -> que los schemas rechacen datos incorrectos.
    Base de datos -> que los modelos guarden, actualicen y borren bien.
    Reglas de negocio -> que no se permita crear duplicados, etc.

    Tests unitarios -> prueban una función o un componente muy pequeño, de forma aislada con el objetivo de verificar que una pieza concreta del código funciona correctamente sin depender de nada externo (base de datos, red, etc.).

    Tests de integración -> prueban cómo interactuán varios componentes juntos (base de datos, modelos, services, crud, etc.) con el objetivo de comprobar que la conexión entre piezas funciona bien.
    Tests de API (End-to-End o E2E) -> prueban la API completa, desde que llega una petición HTTP hasta que devuelve la respuesta con el objetivo de asegurarse de que el sistema entero funciona como el usuario lo usaría.

    --------------------------------------------------------------------------CONFTEST.PY-------------------------------------------------------------------------------
    Dentro de los test; Qué es el archivo conftest.py: es un archivo especial de pytest que se usa para definir configuraciones y fixtures compartidas entre varios tests. Este archivo no hace falta importarlo en cada archivo de test: pytest lo detecta automáticamente, se coloca en la carpeta tests/ y todo lo que defines ahí (por ejemplo, conexiones, datos iniciales, clientes de prueba) estará disponible en los tests.

    --------------------------------------------------------------------------PYTEST.INI--------------------------------------------------------------------------------
    Qué es el archivo pytest.ini: es un archivo de configuración para pytest (la librería más usada en Python para hacer test automáticos), es decir, es como el manual de instrucciones para pytest: le dice dónde buscar los tests, cómo ejecutarlos y qué configuraciones aplicar. Sirve para: definir opciones globales para correr los test, marcar tests especiales (por ejemplo, tests lentos o que necesitan base de datos) y configurar rutas, logs, warnings, etc.

"""

"""
    Cómo funciona el método de .include_router(): sirve para orgnaizar los endpoints en módulos separados y luego "montarlos" dentro de la aplicación principal.

    · Registra todas las rutas de APIRouter en la aplicación principal.
    · Permite añadir un prefijo (prefix="/api") que se antepone a todas las rutas de ese router.
    · Permite establecer etiquetas (tags["api"]) o dependencias comunes.
"""

"""
    Para iniciar el servidor:
    uvicorn app.main:app --reload
"""
import requests
# Importar FastApi de su libreria
from fastapi import FastAPI, Request, Form
# Importar los endpoints desde la API
from app.api import asistencias, clases, usuarios
# Importar la base de datos y la conexión
from app.database.connection import Base, engine, SessionLocal
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.database.connection import obtener_db
from app.models.usuarios import Usuario
from app.services.usuario_services import verificar_contrasena
from starlette.middleware.sessions import SessionMiddleware
from app.init_admin import crear_admin
from datetime import datetime

# Inicializar la API agregando un titulo, descripción y versión para que aparezca en la documentación automática
app = FastAPI(
    title="Gestor de Asistencia",
    description= "API para gestionar estudiantes, profesores, clases y asistencias",
    version="1.0.0"
)

app.add_middleware(SessionMiddleware, secret_key=usuarios.CLAVE_SECRETA)

# Registrar las rutas (endpoints) desde los módulos.
app.include_router(usuarios.router)
app.include_router(clases.router)
app.include_router(asistencias.router)

# Crear todas las tablas definidas
Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

def requerir_sesion(func):
    async def envoltura(request: Request, *args, **kwargs):
        if "usuario" not in request.session:
            return RedirectResponse("/")
        return await func(request, *args, **kwargs)
    return envoltura

@app.on_event("startup")
def iniciar_api():
    db = SessionLocal()
    crear_admin(db)
    db.close()

# Ruta principal de la API
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/inicio_sesion")
def inicio_sesion(request: Request, correo_electronico: str = Form(...), contrasena: str = Form(...)):
    try:
        respuesta = requests.post("http://127.0.0.1:8000/usuarios/inicio_sesion/", data={"username": correo_electronico, "password": contrasena})
        respuesta.raise_for_status()
        datos = respuesta.json()
        token = datos.get("access_token")

        if not token:
            raise Exception("No se recibio el token")
        request.session["token"] = token
        request.session["usuario"] = correo_electronico

        return RedirectResponse("/usuarios", status_code=303)
    except Exception:
        return templates.TemplateResponse("index.html", {"request": request, "error": "Correo electronico o contraseña incorrectos"})

@app.get("/cerrar_sesion")
def cerrar_sesion(request: Request):
    request.session.clear()
    return RedirectResponse("/")

@app.get("/usuarios", response_class=HTMLResponse)
def index(request: Request):
    token = request.session.get("token")
    cabeceras = {"Authorization": f"Bearer {token}"}

    try:
        respuesta = requests.get("http://127.0.0.1:8000/usuarios/", headers=cabeceras)
        respuesta.raise_for_status()
        usuarios = respuesta.json()
    except requests.RequestException:
        usuarios = []

    return templates.TemplateResponse("usuarios.html", {"request": request, "usuarios": usuarios})

@app.get("/crear_usuario", response_class=HTMLResponse)
def pagina_crear_usuario(request: Request):
    return templates.TemplateResponse("crear_usuario.html", {"request": request})

@app.post("/crear_usuario")
def crear_usuario(request: Request, nombre: str = Form(...), apellido: str = Form(...), correo_electronico: str = Form(...), contrasena: str = Form(...), rol: str = Form(...)):
    if not nombre or not apellido or not correo_electronico or not contrasena:
        return templates.TemplateResponse("crear_usuario.html", {"request": request, "error": "Todos los campos son obligatorios"})
    
    try:
        respuesta = requests.post(
            "http://127.0.0.1:8000/usuarios/", 
            json = {
                "nombre": nombre, 
                "apellido": apellido, 
                "correoElectronico": correo_electronico, 
                "contrasena": contrasena,
                "rol": rol
            }
        )
        respuesta.raise_for_status()
        return RedirectResponse("/usuarios", status_code=303)
    except requests.exceptions.RequestException as e:
        return templates.TemplateResponse("crear_usuario.html", {"request": request, "error": f"{str(e)}"})
    
@app.get("/clases", response_class=HTMLResponse)
def index(request: Request):
    try:
        respuesta = requests.get("http://127.0.0.1:8000/clases/")
        respuesta.raise_for_status()
        clases = respuesta.json()
    except requests.RequestException:
        clases = []

    return templates.TemplateResponse("clases.html", {"request": request, "clases": clases})

@app.get("/crear_clase", response_class=HTMLResponse)
def pagina_crear_clase(request: Request):
    return templates.TemplateResponse("crear_clase.html", {"request": request})

@app.post("/crear_clase")
def crear_clase(request: Request, nombre: str = Form(...), fecha: str = Form(...), hora_inicio: str = Form(...), hora_fin: str = Form(...)):
    if not nombre or not fecha or not hora_inicio or not hora_fin:
        return templates.TemplateResponse("crear_clase.html", {"request": request, "error": "Todos los campos son obligatorios"})

    fecha_dt = datetime.strptime(fecha, "%Y-%m-%d").date()
    hora_inicio_dt = datetime.strptime(hora_inicio, "%H:%M").time()
    hora_fin_dt = datetime.strptime(hora_fin, "%H:%M").time()

    token = request.session.get("token")
    cabeceras = {"Authorization": f"Bearer {token}"}

    try:
        respuesta = requests.post(
            "http://127.0.0.1:8000/clases/",
            json={
                "nombre": nombre,
                "fecha": fecha_dt.strftime("%Y-%m-%d"),
                "horaInicio": hora_inicio_dt.strftime("%H:%M"),
                "horaFin": hora_fin_dt.strftime("%H:%M")
            },
            headers=cabeceras
        )
        respuesta.raise_for_status()
        return RedirectResponse("/clases", status_code=303)
    except requests.exceptions.RequestException as e:
        return templates.TemplateResponse("crear_clase.html", {"request": request, "error": f"{str(e)}"})

@app.get("/asistencias", response_class=HTMLResponse)
def index(request: Request):
    try:
        respuesta = requests.get("http://127.0.0.1:8000/asistencias/")
        respuesta.raise_for_status()
        asistencias = respuesta.json()
    except requests.RequestException:
        asistencias = []

    return templates.TemplateResponse("asistencias.html", {"request": request, "asistencias": asistencias})

@app.get("/crear_asistencia", response_class=HTMLResponse)
def pagina_crear_asistencia(request: Request):
    return templates.TemplateResponse("crear_asistencia.html", {"request": request})

@app.post("/crear_asistencia")
def crear_asistencia(request: Request, usuario_id: str = Form(...), clase_id: str = Form(...), estado: str = Form(...)):
    try:
        respuesta = requests.post(
            "http://127.0.0.1:8000/asistencias/",
            json={
                "usuarioId": usuario_id,
                "claseId": clase_id,
                "estado": estado
            }
        )
        respuesta.raise_for_status()
        return RedirectResponse("/asistencias", status_code=303)
    except requests.exceptions.RequestException as e:
        return templates.TemplateResponse("crear_asistencia.html", {"request": request, "error": f"{str(e)}"})