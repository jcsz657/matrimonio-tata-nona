#!/usr/bin/env python3
"""
App Web para Gestión de Gastos del Matrimonio
Una aplicación simple para agregar y monitorear gastos en tiempo real
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Configuración de la página
st.set_page_config(
    page_title="Matrimonio Tata & Nona",
    page_icon="💑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constantes
PRESUPUESTO_TOTAL = 10_000_000
DATOS_DIR = os.path.join(os.path.dirname(__file__), 'datos')
PRESUPUESTO_FILE = os.path.join(DATOS_DIR, 'presupuesto.csv')
INVITADOS_FILE = os.path.join(DATOS_DIR, 'invitados.csv')
HOSPEDAJE_FILE = os.path.join(DATOS_DIR, 'hospedaje.csv')

# Funciones para cargar y guardar datos
@st.cache_data(ttl=1)  # Cache por 1 segundo
def cargar_presupuesto():
    """Carga el archivo de presupuesto"""
    return pd.read_csv(PRESUPUESTO_FILE)

def guardar_presupuesto(df):
    """Guarda el dataframe al archivo CSV con seguridad"""
    return guardar_presupuesto_seguro(df)

def cargar_invitados():
    """Carga el archivo de invitados"""
    return pd.read_csv(INVITADOS_FILE)

def cargar_hospedaje():
    """Carga el archivo de hospedaje"""
    return pd.read_csv(HOSPEDAJE_FILE)

def crear_opciones_gastos(df):
    """Crea lista de opciones para selector de gastos"""
    gastos_reales = df[df['valor_total'] > 0].copy()
    if len(gastos_reales) == 0:
        return [], []

    opciones = []
    indices = []
    for idx, row in gastos_reales.iterrows():
        opciones.append(f"{row['categoria']} - {row['item']} - ${row['valor_total']:,.0f}")
        indices.append(idx)

    return opciones, indices

def crear_backup_automatico():
    """Crea backup diario antes de modificaciones"""
    import os
    from datetime import datetime

    backup_dir = os.path.join(DATOS_DIR, 'backups')
    os.makedirs(backup_dir, exist_ok=True)

    today = datetime.now().strftime('%Y%m%d')
    backup_file = os.path.join(backup_dir, f'presupuesto_{today}.csv')

    # Solo crear backup si no existe uno de hoy
    if not os.path.exists(backup_file):
        import shutil
        try:
            shutil.copy2(PRESUPUESTO_FILE, backup_file)
            return True
        except Exception as e:
            st.warning(f"⚠️ No se pudo crear backup: {str(e)}")
            return False
    return False

def validar_duplicados(df, categoria, item, valor_total, idx_actual=None):
    """Detecta si existe un gasto similar"""
    duplicados = df[
        (df['categoria'] == categoria) &
        (df['item'].str.lower() == item.lower()) &
        (df['valor_total'] == valor_total)
    ]

    # Excluir el índice actual si estamos editando
    if idx_actual is not None:
        duplicados = duplicados[duplicados.index != idx_actual]

    return len(duplicados) > 0

def guardar_presupuesto_seguro(df):
    """Guarda el presupuesto con validaciones y backup"""
    try:
        # Validar estructura del dataframe
        required_columns = ['categoria', 'item', 'valor_total', 'abonado', 'saldo',
                          'confirmado', 'proveedor', 'fecha_limite', 'notas']

        if not all(col in df.columns for col in required_columns):
            raise ValueError("❌ Estructura de datos inválida")

        # Validar que los saldos sean correctos
        df['saldo'] = df['valor_total'] - df['abonado']

        # Crear backup antes de guardar
        crear_backup_automatico()

        # Guardar
        df.to_csv(PRESUPUESTO_FILE, index=False)
        st.cache_data.clear()

        return True

    except Exception as e:
        st.error(f"❌ Error al guardar: {str(e)}")
        return False

# Título principal
st.title("💑 Gestión de Matrimonio - Tata & Nona")
st.markdown("---")

# Sidebar con navegación
st.sidebar.title("📋 Menú")
pagina = st.sidebar.radio(
    "Navegar a:",
    ["🏠 Dashboard", "➕ Agregar Gasto", "✏️ Editar Gastos", "📊 Análisis Detallado", "👥 Invitados", "ℹ️ Información"]
)

# Cargar datos
df_presupuesto = cargar_presupuesto()
df_invitados = cargar_invitados()
df_hospedaje = cargar_hospedaje()

# Calcular métricas
total_comprometido = df_presupuesto['valor_total'].sum()
total_gastado = df_presupuesto['abonado'].sum()
saldo_por_pagar = total_comprometido - total_gastado
disponible = PRESUPUESTO_TOTAL - total_comprometido
porcentaje_usado = (total_comprometido / PRESUPUESTO_TOTAL) * 100 if PRESUPUESTO_TOTAL > 0 else 0

# ============================================================================
# PÁGINA: DASHBOARD PRINCIPAL
# ============================================================================
if pagina == "🏠 Dashboard":
    st.header("📊 Dashboard Principal")

    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="💰 Presupuesto Total",
            value=f"${PRESUPUESTO_TOTAL:,}",
        )

    with col2:
        st.metric(
            label="📤 Comprometido",
            value=f"${total_comprometido:,}",
            delta=f"{porcentaje_usado:.1f}%"
        )

    with col3:
        st.metric(
            label="✅ Pagado",
            value=f"${total_gastado:,}",
        )

    with col4:
        color = "normal"
        if disponible < 0:
            color = "inverse"
        st.metric(
            label="💵 Disponible",
            value=f"${disponible:,}",
            delta=f"Saldo: ${saldo_por_pagar:,}",
            delta_color=color
        )

    # Semáforo de estado
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if porcentaje_usado < 70:
            st.success(f"🟢 Estado: SALUDABLE ({porcentaje_usado:.1f}% usado)")
        elif porcentaje_usado < 90:
            st.warning(f"🟡 Estado: PRECAUCIÓN ({porcentaje_usado:.1f}% usado)")
        else:
            st.error(f"🔴 Estado: ALERTA ({porcentaje_usado:.1f}% usado)")

    # Gráficos
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Distribución del Presupuesto")
        # Gráfico de dona
        if total_comprometido > 0:
            fig_dona = go.Figure(data=[go.Pie(
                labels=['Comprometido', 'Disponible'],
                values=[total_comprometido, max(disponible, 0)],
                hole=.4,
                marker_colors=['#FF6B6B', '#51CF66']
            )])
            fig_dona.update_layout(height=300)
            st.plotly_chart(fig_dona, use_container_width=True)
        else:
            st.info("No hay gastos registrados aún")

    with col2:
        st.subheader("🏷️ Gastos por Categoría")
        if total_comprometido > 0:
            gastos_cat = df_presupuesto.groupby('categoria')['valor_total'].sum()
            fig_cat = px.bar(
                x=gastos_cat.index,
                y=gastos_cat.values,
                labels={'x': 'Categoría', 'y': 'Valor (COP)'},
                color=gastos_cat.index,
                color_discrete_map={'IGLESIA': '#FF6B6B', 'SALON': '#4ECDC4'}
            )
            fig_cat.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig_cat, use_container_width=True)
        else:
            st.info("No hay gastos por categoría aún")

    # Resumen de estado de pagos
    st.markdown("---")
    st.subheader("💳 Estado de Pagos")

    gastos_reales = df_presupuesto[df_presupuesto['valor_total'] > 0].copy()

    if len(gastos_reales) > 0:
        # Calcular gastos por estado
        sin_pagar = gastos_reales[gastos_reales['abonado'] == 0]
        completamente_pagados = gastos_reales[gastos_reales['saldo'] == 0]
        parcialmente_pagados = gastos_reales[(gastos_reales['abonado'] > 0) & (gastos_reales['saldo'] > 0)]

        col_p1, col_p2, col_p3 = st.columns(3)

        with col_p1:
            st.metric(
                "⏳ Sin Pagar",
                len(sin_pagar),
                delta=f"${sin_pagar['valor_total'].sum():,.0f}" if len(sin_pagar) > 0 else None
            )

        with col_p2:
            st.metric(
                "🔄 Pago Parcial",
                len(parcialmente_pagados),
                delta=f"Saldo: ${parcialmente_pagados['saldo'].sum():,.0f}" if len(parcialmente_pagados) > 0 else None
            )

        with col_p3:
            st.metric(
                "✅ Pagados",
                len(completamente_pagados),
                delta=f"${completamente_pagados['valor_total'].sum():,.0f}" if len(completamente_pagados) > 0 else None
            )

    # Lista de gastos recientes
    st.markdown("---")
    st.subheader("📝 Gastos Registrados")

    # Filtrar solo gastos con valor > 0
    gastos_reales = df_presupuesto[df_presupuesto['valor_total'] > 0].copy()

    if len(gastos_reales) > 0:
        # Formatear para mostrar
        gastos_display = gastos_reales[['categoria', 'item', 'valor_total', 'abonado', 'saldo', 'confirmado', 'proveedor']].copy()

        # Agregar columna de estado de pago
        def estado_pago(row):
            if row['abonado'] == 0:
                return '⏳ Sin pagar'
            elif row['saldo'] == 0:
                return '✅ Pagado'
            else:
                porcentaje = (row['abonado'] / row['valor_total'] * 100) if row['valor_total'] > 0 else 0
                return f'🔄 {porcentaje:.0f}%'

        gastos_display['estado_pago'] = gastos_reales.apply(estado_pago, axis=1)

        # Formatear montos
        gastos_display['valor_total'] = gastos_display['valor_total'].apply(lambda x: f"${x:,.0f}")
        gastos_display['abonado'] = gastos_display['abonado'].apply(lambda x: f"${x:,.0f}")
        gastos_display['saldo'] = gastos_display['saldo'].apply(lambda x: f"${x:,.0f}")
        gastos_display['confirmado'] = gastos_display['confirmado'].apply(lambda x: '✅ Confirmado' if x else '⏳ Pendiente')

        # Reordenar columnas
        gastos_display = gastos_display[['categoria', 'item', 'valor_total', 'abonado', 'saldo', 'estado_pago', 'confirmado', 'proveedor']]
        gastos_display.columns = ['Categoría', 'Item', 'Total', 'Pagado', 'Saldo', 'Estado Pago', 'Confirmación', 'Proveedor']

        st.dataframe(gastos_display, use_container_width=True, hide_index=True)
    else:
        st.info("👉 No hay gastos registrados. Ve a '➕ Agregar Gasto' para comenzar.")

    # Resumen de invitados
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    total_invitados = df_invitados['personas'].sum()
    confirmados = df_invitados[df_invitados['confirmado'] == True]['personas'].sum()
    con_hospedaje = df_invitados['hospedaje'].sum()

    with col1:
        st.metric("👥 Total Invitados", total_invitados)
    with col2:
        st.metric("✅ Confirmados", confirmados)
    with col3:
        st.metric("🏨 Con Hospedaje", con_hospedaje)

# ============================================================================
# PÁGINA: AGREGAR GASTO
# ============================================================================
elif pagina == "➕ Agregar Gasto":
    st.header("➕ Agregar Nuevo Gasto")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### Formulario de Gasto")

        # Listas de ítems predefinidos según categoría (FUERA del form para que sea dinámico)
        items_iglesia = [
            "Curso",
            "Ceremonia",
            "Decoración",
            "Argollas",
            "Arras",
            "Ramo Novia",
            "Ramo Tatiana",
            "Azar Novio",
            "Azar Julio",
            "Decoración Carro",
            "Otro (personalizado)..."
        ]

        items_salon = [
            "Salón",
            "Mesas y Sillas",
            "Comida",
            "Pasabocas",
            "Whisky",
            "Cerveza",
            "Champaña",
            "Crema de Whisky",
            "Ponqué",
            "Platos/Tenedores",
            "Decoración",
            "Música y Director",
            "Otro (personalizado)..."
        ]

        # Categoría (FUERA del form para actualización dinámica)
        categoria = st.selectbox(
            "🏷️ Categoría",
            ["IGLESIA", "SALON"],
            help="Selecciona si el gasto es para la iglesia o el salón",
            key="categoria_select"
        )

        # Seleccionar lista según categoría
        items_disponibles = items_iglesia if categoria == "IGLESIA" else items_salon

        # Item - Selectbox dinámico (FUERA del form)
        item_seleccionado = st.selectbox(
            "📝 Nombre del Gasto",
            items_disponibles,
            help="Selecciona el tipo de gasto",
            key="item_select"
        )

        # Si selecciona "Otro", mostrar campo de texto (FUERA del form)
        item_personalizado = ""
        if item_seleccionado == "Otro (personalizado)...":
            item_personalizado = st.text_input(
                "✏️ Escribe el nombre del gasto personalizado",
                placeholder="Ej: Fotógrafo, Video, etc.",
                help="Escribe el nombre de tu gasto personalizado",
                key="item_custom"
            )

        # Determinar el item final
        if item_seleccionado == "Otro (personalizado)...":
            item = item_personalizado
        else:
            item = item_seleccionado

        st.markdown("---")

        with st.form("form_gasto", clear_on_submit=True):

            st.markdown("#### 💰 Información del Pago")

            col_a, col_b = st.columns(2)

            with col_a:
                # Valor total con placeholder
                valor_total = st.number_input(
                    "💰 Valor Total (COP)",
                    min_value=0,
                    value=0,
                    step=50000,
                    help="Costo total del servicio/producto. Usa las flechas o escribe directamente.",
                    format="%d"
                )

            with col_b:
                # Abonado con placeholder
                abonado = st.number_input(
                    "✅ Pagado Hasta Ahora (COP)",
                    min_value=0,
                    value=0,
                    step=50000,
                    help="Cuánto has pagado ya. Deja en 0 si no has pagado nada.",
                    format="%d"
                )

            # Mostrar vista previa solo si hay un valor total
            if valor_total > 0:
                saldo_preview = valor_total - abonado
                porcentaje_pagado = (abonado / valor_total * 100) if valor_total > 0 else 0

                st.markdown("---")
                st.markdown("#### 📊 Vista Previa del Estado de Pago")

                col_r1, col_r2, col_r3 = st.columns(3)

                with col_r1:
                    st.metric("💰 Total", f"${valor_total:,.0f}")

                with col_r2:
                    st.metric("✅ Pagado", f"${abonado:,.0f}")

                with col_r3:
                    st.metric("💵 Saldo", f"${saldo_preview:,.0f}")

                # Barra de progreso visual
                if porcentaje_pagado > 0:
                    st.progress(porcentaje_pagado / 100, text=f"{porcentaje_pagado:.0f}% pagado")
                else:
                    st.progress(0, text="0% pagado")

                # Estado del pago con emoji
                if abonado == 0:
                    st.info("⏳ **Estado:** Sin pagos realizados")
                elif saldo_preview == 0:
                    st.success("✅ **Estado:** Completamente pagado")
                else:
                    st.warning(f"🔄 **Estado:** Pago parcial - Falta ${saldo_preview:,.0f}")

                st.markdown("---")

            # Proveedor
            proveedor = st.text_input(
                "🏢 Proveedor",
                placeholder="Nombre del proveedor/vendedor",
                help="Opcional"
            )

            col_c, col_d = st.columns(2)

            with col_c:
                # Confirmado
                confirmado = st.checkbox(
                    "✅ Servicio Confirmado",
                    help="Marca si el proveedor ya confirmó el servicio"
                )

            with col_d:
                # Fecha límite
                fecha_limite = st.date_input(
                    "📅 Fecha Límite de Pago",
                    help="Opcional"
                )

            # Notas
            notas = st.text_area(
                "📋 Notas",
                placeholder="Información adicional...",
                help="Opcional"
            )

            # Botón submit
            submitted = st.form_submit_button("💾 Guardar Gasto", use_container_width=True)

            if submitted:
                if not item:
                    st.error("⚠️ Por favor ingresa un nombre para el gasto")
                elif valor_total <= 0:
                    st.error("⚠️ El valor total debe ser mayor a 0")
                else:
                    # Validar duplicados
                    if validar_duplicados(df_presupuesto, categoria, item, valor_total):
                        st.warning(f"""
                        ⚠️ **ADVERTENCIA:** Ya existe un gasto similar:
                        - Categoría: {categoria}
                        - Item: {item}
                        - Valor: ${valor_total:,}

                        ¿Estás seguro de que quieres agregar este gasto duplicado?
                        """)

                        # Opción para continuar de todos modos
                        if not st.checkbox("Sí, agregar de todos modos", key="confirmar_duplicado"):
                            st.stop()

                    # Calcular saldo
                    saldo = valor_total - abonado

                    # Crear nueva fila
                    nueva_fila = pd.DataFrame([{
                        'categoria': categoria,
                        'item': item,
                        'valor_total': valor_total,
                        'abonado': abonado,
                        'saldo': saldo,
                        'confirmado': confirmado,
                        'proveedor': proveedor if proveedor else '',
                        'fecha_limite': fecha_limite.strftime('%Y-%m-%d'),
                        'notas': notas if notas else ''
                    }])

                    # Agregar al dataframe
                    df_actualizado = pd.concat([df_presupuesto, nueva_fila], ignore_index=True)

                    # Guardar
                    guardar_presupuesto(df_actualizado)

                    st.success(f"✅ Gasto '{item}' agregado exitosamente!")
                    st.balloons()

                    # Calcular porcentaje pagado
                    porcentaje_pagado = (abonado / valor_total * 100) if valor_total > 0 else 0

                    # Determinar estado del pago
                    if abonado == 0:
                        estado_pago = "⏳ Sin pagos realizados"
                        color_estado = "normal"
                    elif saldo == 0:
                        estado_pago = "✅ Completamente pagado"
                        color_estado = "normal"
                    else:
                        estado_pago = f"🔄 Pago parcial ({porcentaje_pagado:.1f}% pagado)"
                        color_estado = "normal"

                    # Mostrar resumen detallado
                    col_res1, col_res2 = st.columns([2, 1])

                    with col_res1:
                        st.info(f"""
                        **Resumen del gasto agregado:**
                        - 🏷️ Categoría: **{categoria}**
                        - 📝 Item: **{item}**
                        - 💰 Valor Total: **${valor_total:,}**
                        - ✅ Pagado: **${abonado:,}**
                        - 💵 Saldo Pendiente: **${saldo:,}**
                        - 📊 Estado: **{estado_pago}**
                        """)

                    with col_res2:
                        # Mostrar gráfico de dona pequeño
                        if valor_total > 0:
                            fig_pago = go.Figure(data=[go.Pie(
                                labels=['Pagado', 'Pendiente'],
                                values=[abonado, saldo],
                                hole=.6,
                                marker_colors=['#51CF66', '#FF6B6B']
                            )])
                            fig_pago.update_layout(
                                height=200,
                                showlegend=False,
                                margin=dict(l=0, r=0, t=0, b=0)
                            )
                            fig_pago.add_annotation(
                                text=f"{porcentaje_pagado:.0f}%",
                                x=0.5, y=0.5,
                                font_size=20,
                                showarrow=False
                            )
                            st.plotly_chart(fig_pago, use_container_width=True)

                    # Verificar límite de presupuesto
                    nuevo_total_comprometido = df_actualizado['valor_total'].sum()
                    nuevo_porcentaje = (nuevo_total_comprometido / PRESUPUESTO_TOTAL) * 100

                    if nuevo_total_comprometido > PRESUPUESTO_TOTAL:
                        st.error(f"""
                        🚨 **ALERTA CRÍTICA:**
                        Has excedido el presupuesto total en ${nuevo_total_comprometido - PRESUPUESTO_TOTAL:,.0f}

                        Presupuesto: ${PRESUPUESTO_TOTAL:,}
                        Comprometido: ${nuevo_total_comprometido:,}
                        Exceso: ${nuevo_total_comprometido - PRESUPUESTO_TOTAL:,}
                        """)
                    elif nuevo_porcentaje >= 95:
                        st.error(f"🔴 CRÍTICO: Has usado {nuevo_porcentaje:.1f}% del presupuesto")
                    elif nuevo_porcentaje >= 90:
                        st.warning(f"🟡 PRECAUCIÓN: Has usado {nuevo_porcentaje:.1f}% del presupuesto")

    with col2:
        st.markdown("### 💡 Ayuda")
        st.info("""
        **Cómo funciona el sistema de pagos:**

        1. **Valor Total**: El costo completo del servicio/producto

        2. **Pagado Hasta Ahora**: Cuánto has abonado ya
           - Si es 0: Sin pagos realizados ⏳
           - Si es parcial: Pago en progreso 🔄
           - Si es total: Completamente pagado ✅

        3. **Saldo**: Se calcula automáticamente
           - Saldo = Total - Pagado

        4. **Vista Previa**: Verás el estado del pago antes de guardar

        5. **Después de guardar**: Se muestra un resumen detallado con gráfico
        """)

        st.markdown("### 📊 Estados de Pago")
        st.markdown("""
        - ⏳ **Sin pagar**: No se ha realizado ningún pago
        - 🔄 **Pago parcial**: Se ha pagado una parte
        - ✅ **Pagado**: Completamente pagado
        """)

        # Mostrar resumen actual
        st.markdown("### 📊 Estado Actual")
        st.metric("Total Comprometido", f"${total_comprometido:,}")
        st.metric("Disponible", f"${disponible:,}")

        if porcentaje_usado < 70:
            st.success(f"🟢 {porcentaje_usado:.1f}% usado")
        elif porcentaje_usado < 90:
            st.warning(f"🟡 {porcentaje_usado:.1f}% usado")
        else:
            st.error(f"🔴 {porcentaje_usado:.1f}% usado")

# ============================================================================
# PÁGINA: EDITAR GASTOS
# ============================================================================

# Nueva página de Editar Gastos con sistema de Cards

elif pagina == "✏️ Editar Gastos":
    st.header("✏️ Gestión de Gastos")
    st.markdown("Administra tus gastos de forma visual y sencilla")

    # Verificar si hay gastos
    gastos_reales = df_presupuesto[df_presupuesto['valor_total'] > 0].copy()

    if len(gastos_reales) == 0:
        st.info("👉 No hay gastos para editar. Ve a '➕ Agregar Gasto' primero.")
    else:
        # ========== FILTROS ==========
        st.markdown("")
        st.markdown("### 🔍 Filtros")
        st.markdown("Filtra y organiza tus gastos")
        st.markdown("")

        col_filtro1, col_filtro2, col_filtro3 = st.columns(3)

        with col_filtro1:
            filtro_categoria = st.selectbox(
                "Categoría",
                ["Todas", "IGLESIA", "SALON"],
                key="filtro_cat"
            )

        with col_filtro2:
            filtro_estado = st.selectbox(
                "Estado de Pago",
                ["Todos", "Sin Pagar", "Pago Parcial", "Pagado"],
                key="filtro_estado"
            )

        with col_filtro3:
            ordenar_por = st.selectbox(
                "Ordenar por",
                ["Más Reciente", "Mayor Valor", "Mayor Saldo"],
                key="orden"
            )

        # Aplicar filtros
        gastos_filtrados = gastos_reales.copy()

        if filtro_categoria != "Todas":
            gastos_filtrados = gastos_filtrados[gastos_filtrados['categoria'] == filtro_categoria]

        if filtro_estado == "Sin Pagar":
            gastos_filtrados = gastos_filtrados[gastos_filtrados['abonado'] == 0]
        elif filtro_estado == "Pago Parcial":
            gastos_filtrados = gastos_filtrados[(gastos_filtrados['abonado'] > 0) & (gastos_filtrados['saldo'] > 0)]
        elif filtro_estado == "Pagado":
            gastos_filtrados = gastos_filtrados[gastos_filtrados['saldo'] == 0]

        # Ordenar
        if ordenar_por == "Mayor Valor":
            gastos_filtrados = gastos_filtrados.sort_values('valor_total', ascending=False)
        elif ordenar_por == "Mayor Saldo":
            gastos_filtrados = gastos_filtrados.sort_values('saldo', ascending=False)
        else:  # Más reciente
            gastos_filtrados = gastos_filtrados.iloc[::-1]

        st.markdown("")
        st.markdown("")
        st.markdown('<hr style="margin: 1.5rem 0; border: none; border-top: 1px solid #e0e0e0;">', unsafe_allow_html=True)
        st.markdown("")

        # Mostrar contador con mejor estilo
        col_count1, col_count2 = st.columns([1, 3])
        with col_count1:
            st.markdown(f"### {len(gastos_filtrados)}")
            st.markdown("Gasto(s) encontrado(s)")
        with col_count2:
            st.markdown("")

        st.markdown("")

        # ========== CARDS DE GASTOS ==========
        if len(gastos_filtrados) == 0:
            st.info("No hay gastos que coincidan con los filtros seleccionados.")
        else:
            for idx, gasto in gastos_filtrados.iterrows():
                # Calcular estado de pago
                porcentaje_pagado = (gasto['abonado'] / gasto['valor_total'] * 100) if gasto['valor_total'] > 0 else 0

                if gasto['abonado'] == 0:
                    estado_pago = "⏳ Sin Pagar"
                    color_estado = "#FF6B6B"
                elif gasto['saldo'] == 0:
                    estado_pago = "✅ Pagado"
                    color_estado = "#51CF66"
                else:
                    estado_pago = f"🔄 {porcentaje_pagado:.0f}% Pagado"
                    color_estado = "#FFD93D"

                # Color por categoría
                color_cat = "#FF6B6B" if gasto['categoria'] == 'IGLESIA' else "#4ECDC4"

                # Crear card expandible con espaciado
                with st.expander(
                    f"{'💒' if gasto['categoria'] == 'IGLESIA' else '🎉'} **{gasto['item']}**  •  ${gasto['valor_total']:,.0f}  •  {estado_pago}",
                    expanded=False
                ):
                    # Espaciado superior
                    st.markdown("")

                    # Header del card con métricas
                    col_m1, col_m2, col_m3, col_m4 = st.columns(4)

                    with col_m1:
                        st.metric("💰 Total", f"${gasto['valor_total']:,.0f}")

                    with col_m2:
                        st.metric("✅ Pagado", f"${gasto['abonado']:,.0f}")

                    with col_m3:
                        st.metric("💵 Saldo", f"${gasto['saldo']:,.0f}")

                    with col_m4:
                        st.metric("📊 Avance", f"{porcentaje_pagado:.0f}%")

                    # Espaciado antes de la barra
                    st.markdown("")

                    # Barra de progreso con mejor estilo
                    st.progress(porcentaje_pagado / 100, text=f"**{estado_pago}**")

                    # Espaciado después de la barra
                    st.markdown("")
                    st.markdown("")

                    # Separador más sutil
                    st.markdown('<hr style="margin: 1rem 0; border: none; border-top: 1px solid #e0e0e0;">', unsafe_allow_html=True)

                    # Tabs para organizar opciones
                    tab_editar, tab_pago, tab_eliminar = st.tabs(["✏️ Editar", "💰 Registrar Pago", "🗑️ Eliminar"])

                    # ========== TAB: EDITAR ==========
                    with tab_editar:
                        # Espaciado superior
                        st.markdown("")
                        st.markdown("#### ✏️ Editar Información del Gasto")
                        st.markdown("")

                        # Listas de ítems
                        items_iglesia = [
                            "Curso", "Ceremonia", "Decoración", "Argollas", "Arras",
                            "Ramo Novia", "Ramo Tatiana", "Azar Novio", "Azar Julio",
                            "Decoración Carro", "Otro (personalizado)..."
                        ]

                        items_salon = [
                            "Salón", "Mesas y Sillas", "Comida", "Pasabocas",
                            "Whisky", "Cerveza", "Champaña", "Crema de Whisky",
                            "Ponqué", "Platos/Tenedores", "Decoración", "Música y Director",
                            "Otro (personalizado)..."
                        ]

                        # Categoría
                        categoria_edit = st.selectbox(
                            "🏷️ Categoría",
                            ["IGLESIA", "SALON"],
                            index=0 if gasto['categoria'] == 'IGLESIA' else 1,
                            key=f"cat_edit_{idx}"
                        )

                        # Items según categoría
                        items_disponibles = items_iglesia if categoria_edit == "IGLESIA" else items_salon

                        # Determinar índice del item actual
                        item_actual = gasto['item']
                        if item_actual in items_disponibles:
                            item_index = items_disponibles.index(item_actual)
                        else:
                            item_index = len(items_disponibles) - 1

                        item_edit = st.selectbox(
                            "📝 Nombre del Gasto",
                            items_disponibles,
                            index=item_index,
                            key=f"item_edit_{idx}"
                        )

                        # Campo personalizado si es necesario
                        item_personalizado_edit = ""
                        if item_edit == "Otro (personalizado)...":
                            item_personalizado_edit = st.text_input(
                                "✏️ Escribe el nombre del gasto",
                                value=item_actual if item_actual not in items_disponibles else "",
                                key=f"item_custom_edit_{idx}"
                            )

                        # Determinar item final
                        if item_edit == "Otro (personalizado)...":
                            item_final = item_personalizado_edit
                        else:
                            item_final = item_edit

                        # Espaciado antes del formulario
                        st.markdown("")

                        # Formulario de edición
                        with st.form(f"form_editar_{idx}"):
                            st.markdown("**💰 Valores Monetarios**")
                            col_e1, col_e2 = st.columns(2)

                            with col_e1:
                                valor_total_edit = st.number_input(
                                    "💰 Valor Total (COP)",
                                    min_value=0,
                                    value=int(gasto['valor_total']),
                                    step=50000,
                                    key=f"total_edit_{idx}"
                                )

                            with col_e2:
                                abonado_edit = st.number_input(
                                    "✅ Pagado Hasta Ahora (COP)",
                                    min_value=0,
                                    max_value=int(valor_total_edit),
                                    value=int(gasto['abonado']),
                                    step=50000,
                                    key=f"abonado_edit_{idx}"
                                )

                            st.markdown("")
                            st.markdown("**🏢 Información del Proveedor**")

                            proveedor_edit = st.text_input(
                                "Nombre del Proveedor",
                                value=gasto['proveedor'],
                                key=f"prov_edit_{idx}",
                                placeholder="Ej: Floristería La Rosa"
                            )

                            st.markdown("")
                            st.markdown("**📅 Estado y Fechas**")

                            col_e3, col_e4 = st.columns(2)

                            with col_e3:
                                confirmado_edit = st.checkbox(
                                    "✅ Servicio Confirmado",
                                    value=bool(gasto['confirmado']),
                                    key=f"conf_edit_{idx}"
                                )

                            with col_e4:
                                from datetime import datetime
                                try:
                                    fecha_actual = datetime.strptime(gasto['fecha_limite'], '%Y-%m-%d').date()
                                except:
                                    fecha_actual = datetime.now().date()

                                fecha_limite_edit = st.date_input(
                                    "📅 Fecha Límite",
                                    value=fecha_actual,
                                    key=f"fecha_edit_{idx}"
                                )

                            st.markdown("")
                            st.markdown("**📋 Notas Adicionales**")

                            notas_edit = st.text_area(
                                "Información adicional sobre este gasto",
                                value=gasto['notas'],
                                key=f"notas_edit_{idx}",
                                height=100,
                                placeholder="Ej: Pago en 3 cuotas, confirmado por WhatsApp..."
                            )

                            st.markdown("")
                            submitted_edit = st.form_submit_button("💾 Guardar Cambios", type="primary", use_container_width=True)

                            if submitted_edit:
                                if not item_final:
                                    st.error("⚠️ Por favor ingresa un nombre para el gasto")
                                elif valor_total_edit <= 0:
                                    st.error("⚠️ El valor total debe ser mayor a 0")
                                else:
                                    # Calcular nuevo saldo
                                    saldo_edit = valor_total_edit - abonado_edit

                                    # Actualizar el dataframe
                                    df_actualizado = df_presupuesto.copy()
                                    df_actualizado.loc[idx, 'categoria'] = categoria_edit
                                    df_actualizado.loc[idx, 'item'] = item_final
                                    df_actualizado.loc[idx, 'valor_total'] = valor_total_edit
                                    df_actualizado.loc[idx, 'abonado'] = abonado_edit
                                    df_actualizado.loc[idx, 'saldo'] = saldo_edit
                                    df_actualizado.loc[idx, 'confirmado'] = confirmado_edit
                                    df_actualizado.loc[idx, 'proveedor'] = proveedor_edit
                                    df_actualizado.loc[idx, 'fecha_limite'] = fecha_limite_edit.strftime('%Y-%m-%d')
                                    df_actualizado.loc[idx, 'notas'] = notas_edit

                                    # Guardar
                                    guardar_presupuesto(df_actualizado)

                                    st.success(f"✅ Gasto '{item_final}' actualizado exitosamente!")
                                    st.balloons()
                                    import time
                                    time.sleep(1)
                                    st.rerun()

                    # ========== TAB: PAGO RÁPIDO ==========
                    with tab_pago:
                        # Espaciado superior
                        st.markdown("")
                        st.markdown("#### 💰 Registrar Nuevo Pago")
                        st.markdown("")

                        if gasto['saldo'] == 0:
                            st.success("✅ Este gasto ya está completamente pagado.")
                            st.markdown("")
                        else:
                            # Card de saldo pendiente más visual
                            col_saldo1, col_saldo2 = st.columns([2, 1])
                            with col_saldo1:
                                st.info(f"💵 **Saldo pendiente:** ${gasto['saldo']:,.0f}")
                            with col_saldo2:
                                st.metric("Ya pagado", f"{porcentaje_pagado:.0f}%")

                            st.markdown("")

                            with st.form(f"form_pago_{idx}"):
                                nuevo_pago = st.number_input(
                                    "💸 Monto del Pago (COP)",
                                    min_value=0,
                                    max_value=int(gasto['saldo']),
                                    value=0,
                                    step=50000,
                                    key=f"pago_{idx}",
                                    help="Ingresa el monto que acabas de pagar"
                                )

                                st.markdown("")

                                notas_pago = st.text_input(
                                    "📋 Notas del Pago (opcional)",
                                    placeholder="Ej: Pago 2/3, Transferencia bancaria, Efectivo...",
                                    key=f"notas_pago_{idx}"
                                )

                                st.markdown("")
                                submitted_pago = st.form_submit_button("💾 Registrar Pago", type="primary", use_container_width=True)

                                if submitted_pago:
                                    if nuevo_pago <= 0:
                                        st.error("⚠️ El monto debe ser mayor a 0")
                                    else:
                                        # Calcular nuevo abonado y saldo
                                        nuevo_abonado = gasto['abonado'] + nuevo_pago
                                        nuevo_saldo = gasto['valor_total'] - nuevo_abonado

                                        # Actualizar
                                        df_actualizado = df_presupuesto.copy()
                                        df_actualizado.loc[idx, 'abonado'] = nuevo_abonado
                                        df_actualizado.loc[idx, 'saldo'] = nuevo_saldo

                                        # Agregar notas
                                        if notas_pago:
                                            nota_existente = df_actualizado.loc[idx, 'notas']
                                            if nota_existente:
                                                df_actualizado.loc[idx, 'notas'] = f"{nota_existente} | {notas_pago}"
                                            else:
                                                df_actualizado.loc[idx, 'notas'] = notas_pago

                                        # Guardar
                                        guardar_presupuesto(df_actualizado)

                                        st.success(f"✅ Pago de ${nuevo_pago:,.0f} registrado!")
                                        if nuevo_saldo == 0:
                                            st.success("🎉 ¡Gasto completamente pagado!")
                                        st.balloons()
                                        import time
                                        time.sleep(1)
                                        st.rerun()

                    # ========== TAB: ELIMINAR ==========
                    with tab_eliminar:
                        # Espaciado superior
                        st.markdown("")
                        st.markdown("#### 🗑️ Eliminar Gasto")
                        st.markdown("")

                        st.error("""
                        ⚠️ **ADVERTENCIA:** Esta acción es permanente y no se puede deshacer.
                        """)

                        st.markdown("")

                        # Card con información del gasto
                        st.markdown("**📋 Información del gasto a eliminar:**")
                        col_info1, col_info2 = st.columns(2)

                        with col_info1:
                            st.markdown(f"""
                            - 🏷️ **Categoría:** {gasto['categoria']}
                            - 📝 **Item:** {gasto['item']}
                            """)

                        with col_info2:
                            st.markdown(f"""
                            - 💰 **Total:** ${gasto['valor_total']:,.0f}
                            - 🏢 **Proveedor:** {gasto['proveedor']}
                            """)

                        st.markdown("")
                        st.markdown("")

                        # Confirmación para eliminar
                        confirmar_elim = st.checkbox(
                            "⚠️ He leído la advertencia y confirmo que quiero eliminar este gasto",
                            key=f"conf_elim_{idx}"
                        )

                        st.markdown("")

                        col_del1, col_del2 = st.columns(2)

                        with col_del1:
                            if st.button(
                                "🗑️ Eliminar Permanentemente",
                                disabled=not confirmar_elim,
                                type="primary",
                                key=f"btn_elim_{idx}",
                                use_container_width=True
                            ):
                                # Eliminar
                                df_actualizado = df_presupuesto.drop(idx).reset_index(drop=True)
                                guardar_presupuesto(df_actualizado)

                                st.success(f"✅ Gasto '{gasto['item']}' eliminado!")
                                st.info(f"💰 Presupuesto liberado: ${gasto['valor_total']:,.0f}")
                                st.balloons()
                                import time
                                time.sleep(1)
                                st.rerun()

                        with col_del2:
                            st.markdown("")  # Espaciado

                # Espaciado entre cards
                st.markdown("")

        # ========== RESUMEN AL FINAL ==========
        st.markdown("")
        st.markdown("")
        st.markdown('<hr style="margin: 2rem 0; border: none; border-top: 2px solid #e0e0e0;">', unsafe_allow_html=True)
        st.markdown("")
        st.markdown("### 📊 Resumen General")
        st.markdown("Vista consolidada de tu presupuesto")
        st.markdown("")

        col_r1, col_r2, col_r3 = st.columns(3)

        with col_r1:
            st.metric("Total Comprometido", f"${total_comprometido:,}")

        with col_r2:
            st.metric("Total Pagado", f"${total_gastado:,}")

        with col_r3:
            st.metric("Disponible", f"${disponible:,}")


# ============================================================================
# PÁGINA: ANÁLISIS DETALLADO
# ============================================================================
elif pagina == "📊 Análisis Detallado":
    st.header("📊 Análisis Detallado de Gastos")

    gastos_reales = df_presupuesto[df_presupuesto['valor_total'] > 0]

    if len(gastos_reales) == 0:
        st.warning("No hay gastos para analizar aún. Agrega algunos gastos primero.")
    else:
        # Top 10 gastos
        st.subheader("🔝 Top 10 Gastos Más Altos")
        top_10 = gastos_reales.nlargest(10, 'valor_total')

        fig_top = px.bar(
            top_10,
            x='item',
            y='valor_total',
            color='categoria',
            title='Top 10 Gastos',
            labels={'valor_total': 'Valor (COP)', 'item': 'Item'},
            color_discrete_map={'IGLESIA': '#FF6B6B', 'SALON': '#4ECDC4'}
        )
        fig_top.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_top, use_container_width=True)

        # Comparación categorías
        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("💒 IGLESIA")
            iglesia = gastos_reales[gastos_reales['categoria'] == 'IGLESIA']
            if len(iglesia) > 0:
                total_iglesia = iglesia['valor_total'].sum()
                abonado_iglesia = iglesia['abonado'].sum()
                st.metric("Total IGLESIA", f"${total_iglesia:,}")
                st.metric("Pagado", f"${abonado_iglesia:,}")
                st.metric("Pendiente", f"${total_iglesia - abonado_iglesia:,}")
            else:
                st.info("Sin gastos en IGLESIA")

        with col2:
            st.subheader("🎉 SALÓN")
            salon = gastos_reales[gastos_reales['categoria'] == 'SALON']
            if len(salon) > 0:
                total_salon = salon['valor_total'].sum()
                abonado_salon = salon['abonado'].sum()
                st.metric("Total SALÓN", f"${total_salon:,}")
                st.metric("Pagado", f"${abonado_salon:,}")
                st.metric("Pendiente", f"${total_salon - abonado_salon:,}")
            else:
                st.info("Sin gastos en SALÓN")

        # Gastos sin confirmar
        st.markdown("---")
        st.subheader("⏳ Gastos Pendientes por Confirmar")
        sin_confirmar = gastos_reales[gastos_reales['confirmado'] == False]

        if len(sin_confirmar) > 0:
            st.warning(f"Tienes {len(sin_confirmar)} gasto(s) sin confirmar")
            st.dataframe(
                sin_confirmar[['categoria', 'item', 'valor_total', 'proveedor']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("✅ ¡Todos los gastos están confirmados!")

        # Evolución del presupuesto
        st.markdown("---")
        st.subheader("📈 Resumen General")

        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = porcentaje_usado,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "% del Presupuesto Usado"},
            delta = {'reference': 70},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 70], 'color': "lightgreen"},
                    {'range': [70, 90], 'color': "yellow"},
                    {'range': [90, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))

        st.plotly_chart(fig_gauge, use_container_width=True)

# ============================================================================
# PÁGINA: INVITADOS
# ============================================================================
elif pagina == "👥 Invitados":
    st.header("👥 Gestión de Invitados")

    # Métricas
    col1, col2, col3 = st.columns(3)

    total_personas = df_invitados['personas'].sum()
    total_confirmados = df_invitados[df_invitados['confirmado'] == True]['personas'].sum()
    total_hospedaje = df_invitados['hospedaje'].sum()

    with col1:
        st.metric("Total Personas", total_personas)
    with col2:
        st.metric("Confirmados", total_confirmados)
    with col3:
        st.metric("Requieren Hospedaje", total_hospedaje)

    # Gráfico por grupo
    st.markdown("---")
    st.subheader("📊 Invitados por Grupo")

    invitados_grupo = df_invitados.groupby('grupo')['personas'].sum().reset_index()

    fig_grupos = px.bar(
        invitados_grupo,
        x='grupo',
        y='personas',
        color='grupo',
        title='Distribución de Invitados',
        color_discrete_map={'PUENTE': '#FF6B6B', 'BOGOTA': '#4ECDC4', 'CASA': '#95E1D3'}
    )
    st.plotly_chart(fig_grupos, use_container_width=True)

    # Lista de invitados
    st.markdown("---")
    st.subheader("📝 Lista Completa de Invitados")

    # Formatear para display
    inv_display = df_invitados.copy()
    inv_display['confirmado'] = inv_display['confirmado'].apply(lambda x: '✅' if x else '⏳')
    inv_display.columns = ['Nombre', 'Grupo', 'Personas', 'Hospedaje', 'Confirmado', 'Notas']

    st.dataframe(inv_display, use_container_width=True, hide_index=True)

# ============================================================================
# PÁGINA: INFORMACIÓN
# ============================================================================
elif pagina == "ℹ️ Información":
    st.header("ℹ️ Información del Sistema")

    st.markdown("""
    ## 💑 Sistema de Gestión de Matrimonio

    ### ✨ Características:

    - ✅ **Dashboard en tiempo real**: Ve tu presupuesto actualizado al instante
    - ➕ **Agregar gastos fácilmente**: Formulario simple para nuevos gastos
    - 📊 **Análisis visual**: Gráficos interactivos de tus gastos
    - 👥 **Gestión de invitados**: Control de confirmaciones y hospedaje
    - 💾 **Datos persistentes**: Todo se guarda en archivos CSV

    ### 🚀 Cómo usar:

    1. **Dashboard**: Ve el resumen general de tu presupuesto
    2. **Agregar Gasto**: Usa el formulario para registrar nuevos gastos
    3. **Análisis**: Revisa gráficos detallados de tus gastos
    4. **Invitados**: Monitorea las confirmaciones

    ### 📁 Archivos de datos:

    - `datos/presupuesto.csv`: Todos tus gastos
    - `datos/invitados.csv`: Lista de invitados
    - `datos/hospedaje.csv`: Gestión de hospedaje

    ### 💡 Consejos:

    - 🟢 **Verde (<70%)**: Presupuesto saludable
    - 🟡 **Amarillo (70-90%)**: Monitorear cuidadosamente
    - 🔴 **Rojo (>90%)**: ¡Alerta! Revisar urgentemente

    ### 🔄 Actualización automática:

    La app se actualiza automáticamente cuando agregas nuevos gastos.
    Si modificas los archivos CSV manualmente, recarga la página (F5).

    ---

    **Presupuesto Total:** $10,000,000 COP
    **Participantes:** Tata & Nona
    **Versión:** 1.0
    """)

    # Exportar a Excel
    st.markdown("---")
    st.subheader("💾 Exportar Datos")

    if st.button("📥 Descargar Presupuesto (Excel)"):
        # Crear archivo Excel en memoria
        from io import BytesIO
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_presupuesto.to_excel(writer, sheet_name='Presupuesto', index=False)
            df_invitados.to_excel(writer, sheet_name='Invitados', index=False)
            df_hospedaje.to_excel(writer, sheet_name='Hospedaje', index=False)

        output.seek(0)

        st.download_button(
            label="💾 Descargar Excel",
            data=output,
            file_name=f"matrimonio_datos_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # Gestión de backups
    st.markdown("---")
    st.subheader("💾 Gestión de Backups")

    import glob
    backup_dir = os.path.join(DATOS_DIR, 'backups')

    if os.path.exists(backup_dir):
        backups = sorted(glob.glob(os.path.join(backup_dir, 'presupuesto_*.csv')), reverse=True)

        if backups:
            st.success(f"✅ Tienes {len(backups)} backup(s) disponible(s)")

            # Mostrar lista de backups
            st.markdown("**Backups disponibles:**")
            for backup in backups[:5]:  # Mostrar últimos 5
                fecha = os.path.basename(backup).replace('presupuesto_', '').replace('.csv', '')
                fecha_formato = f"{fecha[0:4]}-{fecha[4:6]}-{fecha[6:8]}"
                st.text(f"📅 {fecha_formato}")

            # Opción para restaurar
            st.markdown("---")
            st.warning("""
            ⚠️ **Restaurar backup:**
            Para restaurar un backup, contacta al administrador o copia manualmente
            el archivo desde la carpeta `datos/backups/` a `datos/presupuesto.csv`
            """)
        else:
            st.info("No hay backups disponibles todavía.")
    else:
        st.info("El sistema de backups se creará automáticamente al editar un gasto.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("💑 **Matrimonio Tata & Nona**")
st.sidebar.markdown(f"💰 Presupuesto: ${PRESUPUESTO_TOTAL:,}")
st.sidebar.markdown(f"📊 Usado: {porcentaje_usado:.1f}%")
