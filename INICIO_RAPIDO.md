# Inicio Rápido - Sistema de Gestión de Matrimonio 🚀

Guía de 5 minutos para comenzar a usar el sistema.

## ⚡ Instalación Rápida

### 1. Crear entorno virtual e instalar dependencias (solo una vez)

```bash
cd matrimonio
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Nota:** Cada vez que abras una nueva terminal, debes activar el entorno virtual:
```bash
source venv/bin/activate
```

### 2. Verificar instalación

```bash
python3 scripts/generar_reporte.py
```

Deberías ver un reporte con los datos iniciales.

## 📊 Primer Uso

### Paso 1: Actualizar datos de presupuesto

Abre `datos/presupuesto.csv` con Excel, VSCode o cualquier editor de texto:

```csv
categoria,item,valor_total,abonado,saldo,confirmado,proveedor,fecha_limite,notas
IGLESIA,Ceremonia,500000,200000,300000,False,Parroquia,2026-06-01,
SALON,Comida,3000000,0,3000000,False,Catering XYZ,2026-06-01,
```

**Importante:**
- `saldo` debe ser igual a `valor_total - abonado`
- Fechas en formato: YYYY-MM-DD
- `confirmado` usa `True` o `False`

### Paso 2: Confirmar invitados

Abre `datos/invitados.csv`:

```csv
nombre,grupo,personas,hospedaje,confirmado,notas
Nelly,BOGOTA,3,3,True,Confirmó por WhatsApp
```

Cambia `confirmado` a `True` cuando confirmen asistencia.

### Paso 3: Abrir Dashboard

```bash
cd matrimonio
jupyter notebook
```

1. Navega a `notebooks/`
2. Abre `01_dashboard_principal.ipynb`
3. Click en "Cell" → "Run All"

¡Verás tu dashboard completo con gráficos!

## 🎯 Uso Diario

### Opción A: Dashboard Visual (Recomendado)

```bash
jupyter notebook
# Abrir: notebooks/01_dashboard_principal.ipynb
# Ejecutar todas las celdas
```

### Opción B: Reporte Rápido en Terminal

```bash
python3 scripts/generar_reporte.py
```

### Opción C: Ver Alertas

```bash
python3 scripts/alertas.py
```

## 📋 Flujo de Trabajo Típico

### Cuando recibes una cotización:

1. Abre `datos/presupuesto.csv`
2. Actualiza el `valor_total` del ítem
3. Actualiza `proveedor` con el nombre
4. Guarda el archivo
5. Ejecuta: `python3 scripts/validar_datos.py` (verifica que está bien)
6. Abre el dashboard en Jupyter para ver actualización visual

### Cuando haces un pago:

1. Abre `datos/presupuesto.csv`
2. Actualiza `abonado` sumando el nuevo pago
3. Actualiza `saldo` (valor_total - abonado)
4. Guarda el archivo
5. Verifica: `python3 scripts/generar_reporte.py`

### Cuando confirman invitados:

1. Abre `datos/invitados.csv`
2. Cambia `confirmado` a `True`
3. Agrega notas si quieres
4. Guarda
5. Abre notebook: `notebooks/03_gestion_invitados.ipynb`

## 🆘 Solución de Problemas Rápida

### Error: "command not found: python"
```bash
# Usa python3 en lugar de python
python3 scripts/generar_reporte.py
```

### Error: "ModuleNotFoundError: No module named 'pandas'"
```bash
# Instala las dependencias
pip3 install -r requirements.txt
```

### Jupyter no abre
```bash
# Verifica instalación
jupyter --version

# Si no está instalado
pip3 install jupyter

# Inicia de nuevo
jupyter notebook
```

### Los gráficos no se ven
En la primera celda del notebook, agrega:
```python
%matplotlib inline
```

### Error en CSV: "Expected X columns, got Y"
- Abre el CSV en un editor de texto (no Excel)
- Verifica que no haya comas extra
- Verifica que cada línea tenga el mismo número de campos

## 📝 Atajos Útiles

### En Jupyter Notebooks:
- `Shift + Enter`: Ejecutar celda actual
- `Ctrl + Enter`: Ejecutar celda sin avanzar
- `ESC + A`: Insertar celda arriba
- `ESC + B`: Insertar celda abajo
- `ESC + D + D`: Eliminar celda

### Scripts útiles:
```bash
# Reporte completo
python3 scripts/generar_reporte.py

# Validar datos
python3 scripts/validar_datos.py

# Ver alertas
python3 scripts/alertas.py

# Iniciar Jupyter
jupyter notebook

# Ver esta guía
cat INICIO_RAPIDO.md
```

## 🎯 Próximos Pasos

1. ✅ **Ahora**: Actualiza `presupuesto.csv` con tus cotizaciones reales
2. ✅ **Esta semana**: Explora todos los notebooks
3. ✅ **Cada semana**: Ejecuta `python3 scripts/alertas.py`
4. ✅ **Antes de reuniones**: Genera reportes Excel desde notebooks

## 📚 Más Información

- **Guía completa**: `README.md`
- **Checklist de tareas**: `docs/checklist_preboda.md`
- **Comunicación con proveedores**: `docs/plantillas_proveedores.md`

## 💡 Consejo Final

**Configura un recordatorio semanal:**
```bash
# Cada lunes, ejecuta:
cd matrimonio
python3 scripts/alertas.py
python3 scripts/generar_reporte.py
```

Esto te mantendrá al día con:
- Fechas límite próximas
- Invitados sin confirmar
- Estado del presupuesto
- Hospedajes pendientes

---

## 🎉 ¡Listo!

Ya tienes todo configurado. Comienza actualizando tus datos y explorando el dashboard.

**¿Dudas?** Revisa el `README.md` para documentación completa.

**¡Éxito en la organización de tu matrimonio! 💑**
