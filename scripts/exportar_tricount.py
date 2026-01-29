#!/usr/bin/env python3
"""
Script para exportar datos del matrimonio a formato Tricount
Genera una guía paso a paso para configurar Tricount con los gastos del matrimonio
"""

import pandas as pd
from datetime import datetime

# Configuración
PARTICIPANTES = ["Tata", "Nona"]
PRESUPUESTO_TOTAL = 10_000_000

def cargar_datos():
    """Carga los datos del matrimonio"""
    import os
    # Obtener la ruta del directorio base del proyecto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)

    df_presupuesto = pd.read_csv(os.path.join(base_dir, 'datos', 'presupuesto.csv'))
    df_invitados = pd.read_csv(os.path.join(base_dir, 'datos', 'invitados.csv'))
    return df_presupuesto, df_invitados

def generar_guia_tricount(df_presupuesto):
    """Genera la guía para configurar Tricount"""

    print("="*80)
    print("           GUÍA PARA CONFIGURAR TRICOUNT - MATRIMONIO")
    print("="*80)
    print()

    # Paso 1: Configuración inicial
    print("📱 PASO 1: CREAR EL TRICOUNT")
    print("-" * 80)
    print("1. Entra a https://tricount.com/es-es/ o descarga la app")
    print("2. Haz clic en 'Crear un Tricount'")
    print("3. Nombre sugerido: 'Matrimonio Tata & Nona'")
    print("4. Agrega los participantes:")
    for i, participante in enumerate(PARTICIPANTES, 1):
        print(f"   {i}. {participante}")
    print()

    # Paso 2: Resumen de gastos
    print("📊 PASO 2: RESUMEN DE GASTOS A INGRESAR")
    print("-" * 80)

    # Filtrar solo gastos con valor > 0
    gastos_reales = df_presupuesto[df_presupuesto['valor_total'] > 0].copy()

    if len(gastos_reales) == 0:
        print("⚠️  ATENCIÓN: No hay gastos registrados aún (todos los valores están en $0)")
        print("   Debes actualizar el archivo datos/presupuesto.csv con los valores reales")
        print("   Una vez actualices los valores, vuelve a ejecutar este script")
        print()
        gastos_a_mostrar = df_presupuesto.copy()
        mostrar_plantilla = True
    else:
        gastos_a_mostrar = gastos_reales
        mostrar_plantilla = False

    total_gastos = gastos_a_mostrar['valor_total'].sum()
    total_abonado = gastos_a_mostrar['abonado'].sum()

    print(f"Total de ítems: {len(gastos_a_mostrar)}")
    print(f"Total presupuestado: ${total_gastos:,.0f}")
    print(f"Total abonado hasta ahora: ${total_abonado:,.0f}")
    print()

    # Paso 3: Categorías
    print("📂 PASO 3: GASTOS POR CATEGORÍA")
    print("-" * 80)

    for categoria in ['IGLESIA', 'SALON']:
        cat_gastos = gastos_a_mostrar[gastos_a_mostrar['categoria'] == categoria]
        if len(cat_gastos) > 0:
            cat_total = cat_gastos['valor_total'].sum()
            print(f"\n🏷️  {categoria} - Total: ${cat_total:,.0f}")
            print(f"{'Item':<30} {'Valor Total':>15} {'Abonado':>15} {'Proveedor':<20}")
            print("-" * 80)

            for idx, row in cat_gastos.iterrows():
                item = row['item'][:28]
                valor = f"${row['valor_total']:,.0f}"
                abonado = f"${row['abonado']:,.0f}"
                proveedor = str(row['proveedor'])[:18] if pd.notna(row['proveedor']) else "-"
                print(f"{item:<30} {valor:>15} {abonado:>15} {proveedor:<20}")

    print()

    # Paso 4: Cómo ingresar gastos en Tricount
    print("💰 PASO 4: CÓMO INGRESAR CADA GASTO EN TRICOUNT")
    print("-" * 80)
    print("""
Para cada gasto de la lista anterior, en Tricount:

1. Haz clic en '+ Agregar gasto'
2. Completa los campos:

   📝 Descripción: [Nombre del item, ej: "Salón - Proveedor XYZ"]
   💵 Monto: [valor_total del CSV]
   📅 Fecha: [Fecha del pago o fecha límite]
   👤 Pagado por: [Tata o Nona - quien hizo el pago]
   👥 Para quiénes: [Selecciona ambos si es gasto compartido 50/50]

3. Guarda el gasto

⚡ TIP: Puedes tomar fotos de los recibos y adjuntarlas a cada gasto en Tricount!
    """)

    # Paso 5: Opciones de división
    print("⚖️  PASO 5: OPCIONES DE DIVISIÓN DE GASTOS")
    print("-" * 80)
    print("""
En Tricount tienes varias opciones para dividir gastos:

A) 50/50 (Por defecto):
   - Selecciona ambos participantes (Tata y Nona)
   - Tricount dividirá automáticamente el gasto en partes iguales

B) División personalizada:
   - Si uno paga más que el otro en ciertos ítems
   - Puedes ajustar los porcentajes manualmente

C) Gasto individual:
   - Si solo un participante se beneficia del gasto
   - Selecciona solo a esa persona en "Para quiénes"

💡 RECOMENDACIÓN: Para un matrimonio, lo más común es dividir 50/50
    """)

    # Paso 6: Lista rápida para copiar
    print("📋 PASO 6: LISTA RÁPIDA PARA COPIAR A TRICOUNT")
    print("-" * 80)
    print()

    print("Copia y pega estos gastos en Tricount uno por uno:")
    print()

    for idx, row in gastos_a_mostrar.iterrows():
        if mostrar_plantilla:
            print(f"• {row['item']} - ${row['valor_total']:,.0f} - {row['categoria']} - [VALOR POR DEFINIR]")
        else:
            proveedor = f" ({row['proveedor']})" if pd.notna(row['proveedor']) and row['proveedor'] != '' else ""
            confirmado = "✅" if row['confirmado'] else "⏳"
            print(f"{confirmado} {row['item']}{proveedor} - ${row['valor_total']:,.0f}")

    print()

    # Paso 7: Después de ingresar todo
    print("✅ PASO 7: DESPUÉS DE INGRESAR TODOS LOS GASTOS")
    print("-" * 80)
    print("""
Tricount mostrará automáticamente:

1. 💰 Balance de cada persona:
   - Cuánto pagó cada uno
   - Cuánto debería pagar cada uno
   - Quién le debe a quién

2. 📊 Estadísticas:
   - Total de gastos
   - Gasto promedio
   - Distribución por participante

3. 💸 Liquidación:
   - Tricount calculará la forma más simple de saldar cuentas
   - Ej: "Tata le debe $500,000 a Nona"

4. 🔗 Compartir:
   - Puedes compartir el enlace del Tricount
   - Ambos pueden ver y agregar gastos en tiempo real
    """)

    # Paso 8: Consejos
    print("💡 CONSEJOS PARA USAR TRICOUNT")
    print("-" * 80)
    print("""
1. 📱 Instala la app en ambos teléfonos para acceso rápido
2. 📸 Toma fotos de todos los recibos y adjúntalas en Tricount
3. 🔄 Actualiza los gastos en tiempo real cuando paguen algo
4. 📊 Revisen el balance semanalmente para estar al día
5. 💾 Exporta el resumen final como PDF para sus registros
6. 🔗 Compartan el enlace del Tricount entre ustedes
7. ⏰ Activa notificaciones para ver cuando el otro agrega gastos
    """)

    # Resumen final
    print()
    print("="*80)
    print("                           RESUMEN FINAL")
    print("="*80)
    if mostrar_plantilla:
        print("⚠️  Recuerda actualizar datos/presupuesto.csv con valores reales")
        print("   Luego ejecuta: python3 scripts/exportar_tricount.py")
    else:
        print(f"✅ Tienes {len(gastos_a_mostrar)} gastos listos para ingresar en Tricount")
        print(f"✅ Total a gestionar: ${total_gastos:,.0f}")
        print(f"✅ Participantes: {', '.join(PARTICIPANTES)}")
    print()
    print("🔗 Crea tu Tricount aquí: https://tricount.com/es-es/")
    print("="*80)

def exportar_csv_tricount(df_presupuesto):
    """Exporta un CSV optimizado para importar a Tricount (si fuera posible)"""

    gastos_reales = df_presupuesto[df_presupuesto['valor_total'] > 0].copy()

    if len(gastos_reales) == 0:
        print("\n⚠️  No se puede exportar CSV porque no hay gastos con valores > 0")
        return

    # Crear formato simple para referencia
    export_data = []
    for idx, row in gastos_reales.iterrows():
        proveedor = row['proveedor'] if pd.notna(row['proveedor']) and row['proveedor'] != '' else ""
        descripcion = f"{row['item']}"
        if proveedor:
            descripcion += f" - {proveedor}"

        export_data.append({
            'Descripcion': descripcion,
            'Monto': int(row['valor_total']),
            'Categoria': row['categoria'],
            'Pagado_por': '[TATA o NONA]',
            'Fecha': row['fecha_limite'] if pd.notna(row['fecha_limite']) else '',
            'Estado': 'Confirmado' if row['confirmado'] else 'Pendiente',
            'Abonado': int(row['abonado']),
            'Saldo': int(row['saldo'])
        })

    df_export = pd.DataFrame(export_data)
    filename = f'tricount_gastos_{datetime.now().strftime("%Y%m%d")}.csv'
    df_export.to_csv(filename, index=False, encoding='utf-8-sig')

    print(f"\n✅ Archivo exportado: {filename}")
    print("   Este archivo es solo para tu referencia, úsalo como guía al ingresar")
    print("   los datos en Tricount manualmente.")

def main():
    """Función principal"""
    print("\n")
    df_presupuesto, df_invitados = cargar_datos()
    generar_guia_tricount(df_presupuesto)
    exportar_csv_tricount(df_presupuesto)
    print("\n")

if __name__ == "__main__":
    main()
