# Quiz System - Sistema de Evaluación y Cuestionarios en Django

Proyecto web desarrollado en Django 5.x bajo el patrón de diseño MVT (Modelo-Vista-Template) para la gestión, creación e inspección jerárquica de exámenes, preguntas y alternativas con validación de lógica de negocio en tiempo de ejecución.

---

## Tecnologías Utilizadas
* **Back-End:** Python 3.12 / Django 5.x
* **Base de Datos:** SQLite3 (ORM de Django)
* **Front-End:** HTML5, CSS3, Bootstrap 5 (CDN)
* **Control de Versiones:** Git & GitHub

---

## Arquitectura de Datos y Modelos (`models.py`)

El modelo relacional se compone de tres entidades conectadas jerárquicamente mediante claves foráneas (`ForeignKey`) con reglas de borrado en cascada (`models.CASCADE`):

1. **`Exam` (Entidad Principal):**
   * `title` (`CharField`, max_length=200): Título del examen limitando caracteres por eficiencia de almacenamiento en SQL.
   * `description` (`TextField`): Explicación detallada e instrucciones del examen.
   * `created_at` (`DateTimeField`, auto_now_add=True): Timestamp automático asignado al momento de creación.

2. **`Question` (Entidad Intermedia):**
   * `exam` (`ForeignKey` -> `Exam`, `related_name='questions'`): Relación 1:N con borrado en cascada.
   * `text` (`TextField`): Enunciado completo de la pregunta.
   * `score` (`IntegerField`, default=10): Puntaje asignado. Se fijó un entero con valor predeterminado 10 para asegurar compatibilidad.

3. **`Choice` (Entidad Hoja):**
   * `question` (`ForeignKey` -> `Question`, `related_name='choices'`): Relación 1:N con borrado en cascada.
   * `text` (`CharField`, max_length=200): Texto de la alternativa.
   * `is_correct` (`BooleanField`): Indicador binario para marcar la respuesta correcta.

---

## Regla de Negocio y Validación con Formsets (`forms.py`)

Se implementó una validación personalizada sobreescribiendo `BaseInlineFormSet` mediante la clase `ChoiceInlineFormSet`:

* **Lógica de Control:** Recorre los formularios de alternativas activas enviados en la petición HTTP POST y contabiliza las opciones donde `is_correct == True`.
* **Restricción Estricta:** Exige que **exactamente una** opción sea marcada como correcta por cada pregunta.
* **Garantía de Integridad:** Si el conteo difiere de 1, el método `clean()` lanza un `ValidationError` que frena la transacción antes de impactar la base de datos, evitando registrar datos inconsistentes.

---

## Flujo Completo del Sistema

1. **Gestión Administrativa (`/admin/`):** El administrador registra exámenes, preguntas y opciones de forma anidada mediante formularios `TabularInline`.
2. **Navegación y Consulta Web:** El cliente consulta el listado principal (`exam_list.html`) y accede al detalle del examen (`exam_detail.html`), donde las consultas ORM optimizadas mediante `related_name` renderizan las preguntas y resaltan la clave correcta con componentes de Bootstrap.
3. **Creación y Validación Web:** Al añadir preguntas desde la interfaz web (`/add-question/`), la vista procesa el `ChoiceFormSet`. Si no hay exactamente una opción correcta, la interfaz muestra una alerta de error sin guardar datos en la BD. Al corregirlo, se persiste en SQLite3 y se redirige a la vista detallada del examen.

---

## Panel de Administración (`admin.py`)

Se configuró una interfaz administrativa personalizada usando `admin.TabularInline` para `ChoiceInline` y `QuestionInline`. Esto permite gestionar la jerarquía completa (Examen -> Preguntas -> Alternativas) desde un solo formulario integrado.

---

## Observaciones sobre Migraciones

* **`0001_initial.py`:** Migración inicial generada con `python manage.py makemigrations quiz`. Registra la estructura relacional de las tablas `quiz_exam`, `quiz_question` y `quiz_choice`.
* **Efecto en Base de Datos:** Aplicada mediante `python manage.py migrate`. Django tradujo las clases Python a sentencias DDL en SQLite3, garantizando índices de rendimiento y claves foráneas en cascada. Todas las migraciones se encuentran versionadas dentro de `quiz/migrations/`.

---

## Instrucciones de Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/SebastianEspiritu/lab03-desarrollo-web-Espiritu-B.git](https://github.com/SebastianEspiritu/lab03-desarrollo-web-Espiritu-B.git)
   cd lab03-desarrollo-web-Espiritu-B

2. Activar el entorno virtual e instalar dependencias:
   ```bash
   .\venv\Scripts\activate
   pip install -r requirements.txt

3. Aplicar migraciones e iniciar el servidor:
   ```bash
   cd src
   python manage.py migrate
   python manage.py runserver

4. CRutas de acceso:

   Vista Pública: http://127.0.0.1:8000/

   Panel de Administración: http://127.0.0.1:8000/admin/


## Historial de commits

feat: add quiz models and run migrations

feat: implement BaseInlineFormSet logic for exact correct choice

feat: add forms, views, urls and HTML templates for quiz management

feat: configure django admin, inlineformsets and test web validation
