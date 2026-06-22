# Sistema de gestión de turnos – Materia Desarrollo de Software

**Grupo 1**

**Integrantes:**
- Bonacorsi Gonzalo
- Ragonese Gian

---

## 🚀 Cómo ejecutar el proyecto localmente

Sigue estos pasos para levantar el servidor de desarrollo en tu computadora:

### 1. Clonar el repositorio
Abre tu terminal y clona el proyecto (si aún no lo has bajado):
```bash
git clone https://github.com/pvillalba91/sistema-turnos-grupo-1-
cd sistema-turnos-grupo-1-
```

### 2. Crear y activar un entorno virtual (Recomendado)
Para mantener las dependencias aisladas, crea un entorno virtual en la raíz del proyecto:
```bash
python -m venv venv
```
Actívalo dependiendo de tu sistema operativo:
* **Windows:**
  ```bash
  .\venv\Scripts\activate
  ```
* **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Instalar dependencias
Con el entorno activado, instala Django y las librerías necesarias:
```bash
pip install django
```
*(Opcional) Si existe un archivo requirements.txt en el proyecto, ejecuta:*
```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones
Prepara la base de datos local con los modelos del proyecto:
```bash
python manage.py migrate
```

### 5. Levantar el servidor
Ejecuta el servidor de desarrollo de Django:
```bash
python manage.py runserver
```

🌐 **¡Listo!** Abre tu navegador web de preferencia y entra a: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
