# sistema-turnos-grupo-1-
Sistema de gestión de turnos – Materia Desarrollo de Software
# Integrantes:

#  - Bonacorsi Gonzalo
#  - Ragonese Gian


# Cómo ejecutar el proyecto localmente:

Sigue estos pasos para levantar el servidor de desarrollo en tu computadora:

# 1. Clonar el repositorio

Abre tu terminal y clona el proyecto (si aún no lo has bajado):

bash
git clone https://github.com/pvillalba91/sistema-turnos-grupo-1-
cd sistema-turnos-grupo-1-


2. Crear y activar un entorno virtual (Recomendado)
Para mantener las dependencias aisladas, crea un entorno virtual en la raíz del proyecto:

Bash
python -m venv venv
Actívalo dependiendo de tu sistema operativo:

Windows:

Bash
.\venv\Scripts\activate
Mac/Linux:

Bash
source venv/bin/activate
3. Instalar dependencias
Con el entorno activado, instala Django y las librerías necesarias:

Bash
pip install django
# (Opcional) Si existe un archivo requirements.txt en el proyecto, ejecuta:
# pip install -r requirements.txt
4. Aplicar migraciones
Prepara la base de datos local con los modelos del proyecto:

Bash
python manage.py migrate
5. Levantar el servidor
Ejecuta el servidor de desarrollo de Django:

Bash
python manage.py runserver
🌐 ¡Listo! Abre tu navegador web de preferencia y entra a: http://127.0.0.1:8000/
