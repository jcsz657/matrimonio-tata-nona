# Sistema de Gestión de Matrimonio 💑

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://matrimonio-tata-nona.streamlit.app)
[![GitHub](https://img.shields.io/badge/GitHub-jcsz657%2Fmatrimonio--tata--nona-blue?logo=github)](https://github.com/jcsz657/matrimonio-tata-nona)

Sistema completo de planificación y gestión de matrimonio con presupuesto de **$10,000,000 COP**, gestión de 40 invitados (21 con hospedaje), control de presupuesto en tiempo real y análisis con Jupyter Notebooks.

## 🌐 Acceso Rápido

**🚀 [Abrir Aplicación Web](https://matrimonio-tata-nona.streamlit.app)** ← Haz clic aquí para usar la app sin instalar nada

> La aplicación web es la forma más fácil de usar el sistema. No necesitas instalar Python ni ninguna dependencia.

## 📋 Contenido

- [Acceso Rápido](#acceso-rápido)
- [Deploy en Streamlit Cloud](#-deploy-en-streamlit-cloud)
- [Instalación Local](#-instalación-local)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Guía de Uso](#guía-de-uso)
- [Actualizar Datos](#actualizar-datos)
- [Notebooks Disponibles](#notebooks-disponibles)
- [Scripts de Utilidad](#scripts-de-utilidad)
- [Consejos y Mejores Prácticas](#consejos-y-mejores-prácticas)

## ☁️ Deploy en Streamlit Cloud

La forma más fácil de compartir la aplicación con otras personas es deployarla en Streamlit Cloud (GRATIS):

### Pasos para deployar:

1. **Crea una cuenta en Streamlit Cloud** (si no la tienes):
   - Ve a [share.streamlit.io](https://share.streamlit.io)
   - Inicia sesión con tu cuenta de GitHub

2. **Deploy la app**:
   - Haz clic en "New app"
   - Selecciona tu repositorio: `jcsz657/matrimonio-tata-nona`
   - Branch: `master`
   - Main file path: `app_matrimonio.py`
   - Haz clic en "Deploy!"

3. **Tu app estará disponible en**:
   ```
   https://matrimonio-tata-nona.streamlit.app
   ```

4. **Compartir por WhatsApp**:
   - Copia este mensaje y envíalo:
   ```
   🎉 ¡Hola! Te invito a ver nuestra app de planificación del matrimonio:

   👉 https://matrimonio-tata-nona.streamlit.app

   Aquí puedes ver el presupuesto, invitados y todos los detalles. ¡Échale un vistazo! 💑
   ```

### Actualizar la app después de cambios:

Cada vez que hagas `git push` a GitHub, la app se actualizará automáticamente en Streamlit Cloud.

```bash
git add .
git commit -m "Actualizar datos"
git push origin master
```

---

## 🚀 Instalación Local

### 1. Requisitos previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### 2. Crear entorno virtual (recomendado)

```bash
cd matrimonio
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

Las dependencias incluyen:
- `jupyter`: Para ejecutar los notebooks interactivos
- `pandas`: Manejo de datos CSV
- `matplotlib` y `seaborn`: Visualizaciones
- `openpyxl`: Exportación a Excel

### 4. Verificar instalación

```bash
# Activar entorno virtual (si no está activado)
source venv/bin/activate

# Verificar que Streamlit está instalado
streamlit --version

# Generar reporte de prueba
python3 scripts/generar_reporte.py
```

### 5. Ejecutar la aplicación web localmente

```bash
# Asegúrate de estar en la carpeta del proyecto
cd matrimonio

# Activar entorno virtual
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Iniciar la aplicación
streamlit run app_matrimonio.py

# O usa el script de inicio:
./iniciar_app.sh
```

La app se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📁 Estructura del Proyecto

```
matrimonio/
├── README.md                          # Esta guía
├── requirements.txt                   # Dependencias Python
├── datos/                             # Datos del matrimonio
│   ├── invitados.csv                 # Lista de invitados
│   ├── presupuesto.csv               # Control de gastos
│   └── hospedaje.csv                 # Gestión de hospedaje
├── notebooks/                         # Notebooks Jupyter
│   ├── 01_dashboard_principal.ipynb  # Dashboard con gráficos
│   ├── 02_analisis_presupuesto.ipynb # Análisis detallado
│   ├── 03_gestion_invitados.ipynb    # Gestión de invitados
│   └── 04_hospedaje.ipynb            # Planificación de hospedaje
├── scripts/                           # Scripts de utilidad
│   ├── generar_reporte.py            # Reporte rápido en terminal
│   ├── validar_datos.py              # Validaciones de integridad
│   └── alertas.py                    # Sistema de alertas
└── docs/                              # Documentación adicional
    ├── checklist_preboda.md          # Lista de tareas
    └── plantillas_proveedores.md     # Plantillas de comunicación
```

## 📖 Guía de Uso

### Iniciar Jupyter Notebooks

```bash
cd matrimonio
jupyter notebook
```

Esto abrirá tu navegador con la interfaz de Jupyter. Navega a la carpeta `notebooks/` y abre el notebook que desees usar.

### Ejecutar Notebooks

1. Abre el notebook deseado (recomendamos empezar con `01_dashboard_principal.ipynb`)
2. Ejecuta las celdas secuencialmente con `Shift + Enter`
3. O ejecuta todas las celdas: Menu → Cell → Run All

## 📝 Actualizar Datos

### 1. Actualizar Presupuesto

Edita el archivo `datos/presupuesto.csv` con un editor de texto o Excel:

```csv
categoria,item,valor_total,abonado,saldo,confirmado,proveedor,fecha_limite,notas
IGLESIA,Ceremonia,500000,200000,300000,True,Parroquia San José,2026-06-01,Confirmado
```

**Campos:**
- `categoria`: IGLESIA o SALON
- `item`: Nombre del gasto
- `valor_total`: Costo total del servicio
- `abonado`: Cuánto has pagado
- `saldo`: Lo que falta por pagar (debe ser = valor_total - abonado)
- `confirmado`: True/False si el servicio está confirmado
- `proveedor`: Nombre del proveedor
- `fecha_limite`: Fecha en formato YYYY-MM-DD
- `notas`: Notas adicionales

### 2. Actualizar Invitados

Edita `datos/invitados.csv`:

```csv
nombre,grupo,personas,hospedaje,confirmado,notas
Nelly,BOGOTA,3,3,True,Vegetariana
```

**Campos:**
- `grupo`: PUENTE, BOGOTA o CASA
- `personas`: Número total de personas
- `hospedaje`: Cuántas requieren hospedaje
- `confirmado`: True/False si confirmaron asistencia

### 3. Actualizar Hospedaje

Edita `datos/hospedaje.csv`:

```csv
nombre_invitado,personas_hospedaje,tipo_habitacion,asignado,costo_estimado,notas
Nelly,3,Suite Triple,True,300000,Hotel Central
```

## 📊 Notebooks Disponibles

### 1. Dashboard Principal (`01_dashboard_principal.ipynb`)

**Usa este notebook para:**
- Ver resumen ejecutivo del matrimonio
- Monitorear estado del presupuesto con semáforo (🟢🟡🔴)
- Visualizar distribución de gastos
- Revisar alertas y pendientes

**Cuándo usarlo:** Diariamente para monitoreo general.

### 2. Análisis de Presupuesto (`02_analisis_presupuesto.ipynb`)

**Usa este notebook para:**
- Desglose detallado IGLESIA vs SALÓN
- Proyección de gastos faltantes
- Identificar ítems sin confirmar
- Exportar reportes a Excel

**Cuándo usarlo:** Al actualizar presupuesto o antes de reuniones con proveedores.

### 3. Gestión de Invitados (`03_gestion_invitados.ipynb`)

**Usa este notebook para:**
- Lista completa de invitados por grupo
- Estadísticas de confirmación
- Calcular costos por persona
- Identificar pendientes por confirmar

**Cuándo usarlo:** Al recibir confirmaciones o antes de contactar invitados.

### 4. Hospedaje (`04_hospedaje.ipynb`)

**Usa este notebook para:**
- Calcular habitaciones necesarias
- Asignar hospedajes
- Estimar costos de hospedaje
- Monitorear pendientes

**Cuándo usarlo:** Al planificar y reservar hoteles.

## 🛠️ Scripts de Utilidad

### Generar Reporte Rápido

```bash
python scripts/generar_reporte.py
```

Muestra un resumen ejecutivo en terminal con:
- Estado del presupuesto
- Invitados confirmados/pendientes
- Hospedajes asignados/pendientes
- Alertas activas

**Uso:** Para chequeo rápido sin abrir notebooks.

### Validar Datos

```bash
python scripts/validar_datos.py
```

Valida integridad de datos:
- Verifica que `saldo = valor_total - abonado`
- Detecta valores negativos
- Valida fechas
- Verifica consistencia entre archivos

**Uso:** Después de actualizar CSV para detectar errores.

### Sistema de Alertas

```bash
python scripts/alertas.py
```

Muestra alertas organizadas por prioridad:
- 🔴 **Críticas**: Presupuesto >90%, fechas vencidas
- ⚠️ **Urgentes**: Fechas límite <15 días
- 🟡 **Advertencias**: Pendientes varios

**Uso:** Semanalmente para monitoreo proactivo.

## 💡 Consejos y Mejores Prácticas

### Flujo de trabajo recomendado

1. **Al inicio del día:**
   ```bash
   python scripts/generar_reporte.py
   python scripts/alertas.py
   ```

2. **Al actualizar datos:**
   - Edita los CSV con los nuevos datos
   - Ejecuta `python scripts/validar_datos.py` para verificar
   - Abre el notebook relevante y ejecuta todas las celdas (Cell → Run All)

3. **Antes de reuniones:**
   - Genera reportes Excel desde los notebooks
   - Revisa dashboard principal para métricas clave

4. **Semanalmente:**
   - Revisa todos los notebooks
   - Actualiza confirmaciones de invitados
   - Verifica fechas límite próximas

### Mantener presupuesto bajo control

- 🟢 **Verde (<70%)**: Presupuesto saludable
- 🟡 **Amarillo (70-90%)**: Monitorear gastos cuidadosamente
- 🔴 **Rojo (>90%)**: ¡Alerta! Revisar urgentemente

**Recomendación:** Mantén un colchón del 10% (~$1,000,000) para imprevistos.

### Backup de datos

Los archivos CSV son tu base de datos. Haz backup regularmente:

```bash
# Crear backup
cp -r datos datos_backup_$(date +%Y%m%d)

# O subirlos a la nube (Google Drive, Dropbox, etc.)
```

### Tips para Excel

Si prefieres editar en Excel:
1. Abre el CSV en Excel
2. Edita los datos
3. **Importante:** Guarda como CSV (no como .xlsx)
4. Verifica que las fechas se guarden en formato YYYY-MM-DD

## ❓ Solución de Problemas

### "ModuleNotFoundError"

```bash
pip install -r requirements.txt
```

### "FileNotFoundError"

Asegúrate de ejecutar comandos desde la carpeta `matrimonio/`:

```bash
cd matrimonio
python scripts/generar_reporte.py
```

### Los gráficos no se muestran

En Jupyter, asegúrate de tener esta línea al inicio:
```python
%matplotlib inline
```

### Errores en CSV

Ejecuta el validador:
```bash
python scripts/validar_datos.py
```

## 📞 Soporte

Para problemas o preguntas:
1. Revisa los mensajes de error en los notebooks
2. Ejecuta `python scripts/validar_datos.py` para detectar problemas
3. Verifica que los CSV estén correctamente formateados

## 🎉 ¡Éxito en tu Matrimonio!

Este sistema te ayudará a mantener todo organizado y bajo control. Recuerda:
- Actualiza datos regularmente
- Revisa alertas semanalmente
- Mantén backups de tus datos
- ¡Disfruta el proceso de planificación!

---

**Versión:** 1.0
**Presupuesto:** $10,000,000 COP
**Invitados:** 40 personas (21 con hospedaje)
