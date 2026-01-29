# 🎉 Cómo Usar la App Web del Matrimonio

## 🚀 Inicio Rápido

### Opción 1: Script de inicio (Recomendado)
```bash
./iniciar_app.sh
```

### Opción 2: Comando manual
```bash
cd matrimonio
source venv/bin/activate
streamlit run app_matrimonio.py
```

## 📱 Acceder a la App

Después de iniciar, la app se abrirá automáticamente en tu navegador en:
```
http://localhost:8501
```

Si no se abre automáticamente, copia y pega esa URL en tu navegador.

## 🎯 Funcionalidades

### 1️⃣ Dashboard (🏠)
- **Ver resumen en tiempo real** de tu presupuesto
- **Semáforo visual**: 🟢 Verde (<70%), 🟡 Amarillo (70-90%), 🔴 Rojo (>90%)
- **Gráficos interactivos**: Distribución por categoría, gastos por ítem
- **Métricas principales**: Total, comprometido, pagado, disponible
- **Lista de invitados**: Confirmaciones y hospedaje

### 2️⃣ Agregar Gasto (➕)
**Formulario simple para nuevos gastos:**
1. Selecciona categoría (IGLESIA o SALON)
2. Nombre del gasto
3. Valor total y cuánto has pagado
4. Proveedor (opcional)
5. Confirmar si está confirmado
6. Fecha límite (opcional)
7. Notas adicionales

**El sistema calcula automáticamente:**
- Saldo pendiente
- Porcentaje usado del presupuesto
- Te alerta si te acercas al límite

### 3️⃣ Análisis Detallado (📊)
- **Top 10 gastos** más altos
- **Comparación IGLESIA vs SALÓN**: Totales, pagado, pendiente
- **Gastos sin confirmar**: Ve qué falta por confirmar
- **Medidor de presupuesto**: Gauge visual del % usado

### 4️⃣ Invitados (👥)
- **Estadísticas**: Total, confirmados, con hospedaje
- **Gráfico por grupo**: PUENTE, BOGOTA, CASA
- **Lista completa** de invitados

### 5️⃣ Información (ℹ️)
- Guía de uso completa
- **Exportar a Excel**: Descarga todos tus datos en un archivo Excel

## 💡 Casos de Uso

### Agregar un gasto nuevo
1. Ve a "➕ Agregar Gasto"
2. Llena el formulario
3. Haz clic en "💾 Guardar Gasto"
4. ¡Listo! Verás el resumen actualizado

### Monitorear el presupuesto
1. Ve al Dashboard
2. Revisa el semáforo de estado
3. Mira los gráficos de distribución
4. Verifica el saldo disponible

### Hacer seguimiento
1. Ve a "📊 Análisis Detallado"
2. Revisa los gastos pendientes por confirmar
3. Compara IGLESIA vs SALÓN
4. Usa el gauge para ver el % usado

### Exportar todo
1. Ve a "ℹ️ Información"
2. Haz clic en "📥 Descargar Presupuesto (Excel)"
3. Descarga el archivo Excel con todo

## ⚙️ Características Técnicas

- ✅ **Datos persistentes**: Todo se guarda en `datos/presupuesto.csv`
- ✅ **Actualización automática**: La app se actualiza al guardar
- ✅ **Gráficos interactivos**: Usa Plotly para visualizaciones
- ✅ **Responsive**: Funciona en desktop y tablet
- ✅ **Sin internet**: Funciona 100% local

## 🔄 Actualizar Datos Manualmente

Si prefieres editar los CSV directamente:

1. Edita `datos/presupuesto.csv` con Excel o editor de texto
2. Guarda los cambios
3. Recarga la página en el navegador (F5)

## 🛑 Detener la App

En la terminal donde corre la app, presiona:
```
Ctrl + C
```

## ❓ Solución de Problemas

### "ModuleNotFoundError: No module named 'streamlit'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### La app no abre en el navegador
Abre manualmente: http://localhost:8501

### Los cambios no se reflejan
Presiona F5 en el navegador o haz clic en "Rerun" en la esquina superior derecha

### Error al guardar
Verifica que tienes permisos de escritura en la carpeta `datos/`

## 💾 Backup

Haz backup regular de tus datos:
```bash
cp -r datos datos_backup_$(date +%Y%m%d)
```

## 🎨 Personalización

Los datos se guardan en archivos CSV simples:
- `datos/presupuesto.csv` - Gastos
- `datos/invitados.csv` - Invitados
- `datos/hospedaje.csv` - Hospedaje

Puedes editarlos directamente con Excel o cualquier editor de texto.

## 🎉 ¡Disfruta planificando tu matrimonio!

Esta app te ayudará a mantener todo organizado y bajo control.

---

**Presupuesto:** $10,000,000 COP
**Participantes:** Tata & Nona
**Versión:** 1.0
