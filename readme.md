# ORGÁNOS FELICES - Instrucciones de ejecución local

Integrantes
- Jesús Eliseo Colunga Martínez
- Marco Emiliano Portillo Martínez

Requisitos
- Python 3.8+ instalado.
- MySQL (server) accesible y credenciales de usuario con privilegios para crear bases.
- (Opcional) entorno virtual recomendado.

1) Crear/activar entorno virtual (Windows - PowerShell)
```powershell
# Si no tienes venv
py -3 -m venv venv

# Activar (PowerShell)
.\venv\Scripts\Activate.ps1

# o (cmd)
.\venv\Scripts\activate
```

2) Instalar dependencias
```powershell
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

3) Crear base de datos y tablas (usar el script create_db.sql)
- Usando MySQL CLI (ejecutar desde la raíz del proyecto):
```powershell
mysql -u root -p < "c:\{RUTA DEL PROYECTO}\create_db.sql"
```
- O abrir `create_db.sql` en MySQL Workbench y ejecutar las sentencias.

4) Ajustar credenciales (si aplica)
- Por defecto el proyecto usa las credenciales fijas en `src\db\db.py`:
  - host: localhost
  - user: root
  - password: 1234
  - db: organos_felices
- Editar `src\db\db.py` si necesita otras credenciales o puerto.

5) Ejecutar la aplicación (GUI)
```powershell
# Desde la raíz del proyecto
py principal.py
```

6) Ejecutar pruebas (pytest)
```powershell
# Desde la raíz del proyecto
py -m pytest test -q
```

7) Ejecutar pylint y generar reporte
```powershell
# Asegurarse de que PYTHONPATH incluye la raíz del proyecto para resolver imports
$env:PYTHONPATH = "C:\{RUTA DEL PROYECTO}"
py -m pylint src > pylint_report.txt
```
