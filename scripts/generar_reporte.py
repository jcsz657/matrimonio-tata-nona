#!/usr/bin/env python3
"""
Script para generar reporte rápido del matrimonio en terminal.
Uso: python scripts/generar_reporte.py
"""

import pandas as pd
import sys
from pathlib import Path

# Añadir directorio de datos al path
DATOS_DIR = Path(__file__).parent.parent / 'datos'
PRESUPUESTO_TOTAL = 10_000_000


def cargar_datos():
    """Carga los archivos CSV de datos."""
    try:
        df_presupuesto = pd.read_csv(DATOS_DIR / 'presupuesto.csv')
        df_invitados = pd.read_csv(DATOS_DIR / 'invitados.csv')
        df_hospedaje = pd.read_csv(DATOS_DIR / 'hospedaje.csv')
        return df_presupuesto, df_invitados, df_hospedaje
    except FileNotFoundError as e:
        print(f"❌ Error: No se pudo encontrar el archivo {e.filename}")
        sys.exit(1)


def generar_reporte():
    """Genera el reporte completo en terminal."""
    df_presupuesto, df_invitados, df_hospedaje = cargar_datos()

    # Calcular métricas de presupuesto
    total_comprometido = df_presupuesto['valor_total'].sum()
    total_abonado = df_presupuesto['abonado'].sum()
    total_saldo = df_presupuesto['saldo'].sum()
    disponible = PRESUPUESTO_TOTAL - total_comprometido
    porcentaje_usado = (total_comprometido / PRESUPUESTO_TOTAL) * 100

    # Calcular métricas de invitados
    total_invitados = df_invitados['personas'].sum()
    confirmados = df_invitados[df_invitados['confirmado'] == True]['personas'].sum()
    pendientes_invitados = total_invitados - confirmados
    total_hospedaje = df_invitados['hospedaje'].sum()

    # Calcular métricas de hospedaje
    hospedajes_asignados = df_hospedaje[df_hospedaje['asignado'] == True]['personas_hospedaje'].sum()
    hospedajes_pendientes = df_hospedaje[df_hospedaje['asignado'] == False]['personas_hospedaje'].sum()
    costo_hospedaje = df_hospedaje['costo_estimado'].sum()

    # Determinar estado
    if porcentaje_usado < 70:
        estado = '🟢 VERDE'
        mensaje = 'Presupuesto saludable'
    elif porcentaje_usado < 90:
        estado = '🟡 AMARILLO'
        mensaje = 'Precaución - monitorear gastos'
    else:
        estado = '🔴 ROJO'
        mensaje = 'ALERTA - presupuesto comprometido'

    # Imprimir reporte
    print("\n" + "=" * 70)
    print(" " * 20 + "RESUMEN MATRIMONIO")
    print("=" * 70)

    print(f"\n💰 PRESUPUESTO:")
    print(f"   Total:                 ${PRESUPUESTO_TOTAL:>15,}")
    print(f"   Comprometido:          ${total_comprometido:>15,.0f} ({porcentaje_usado:.1f}%)")
    print(f"   Abonado:               ${total_abonado:>15,.0f}")
    print(f"   Saldo por pagar:       ${total_saldo:>15,.0f}")
    print(f"   Disponible:            ${disponible:>15,.0f}")
    print(f"\n   Estado: {estado} - {mensaje}")

    print(f"\n👥 INVITADOS:")
    print(f"   Total personas:        {total_invitados:>15}")
    print(f"   Confirmados:           {confirmados:>15} ({confirmados/total_invitados*100:.1f}%)")
    print(f"   Pendientes:            {pendientes_invitados:>15}")

    print(f"\n🏨 HOSPEDAJE:")
    print(f"   Requieren hospedaje:   {total_hospedaje:>15}")
    print(f"   Asignados:             {hospedajes_asignados:>15}")
    print(f"   Pendientes:            {hospedajes_pendientes:>15}")
    if costo_hospedaje > 0:
        print(f"   Costo estimado:        ${costo_hospedaje:>14,.0f}")

    # Alertas
    print(f"\n⚠️  ALERTAS:")
    alertas = []

    if porcentaje_usado > 90:
        alertas.append("   🔴 Presupuesto crítico (>90% usado)")
    elif porcentaje_usado > 70:
        alertas.append("   🟡 Presupuesto en precaución (>70% usado)")

    items_sin_confirmar = df_presupuesto[df_presupuesto['confirmado'] == False]
    if len(items_sin_confirmar) > 0:
        alertas.append(f"   ⚠️  {len(items_sin_confirmar)} ítems de presupuesto sin confirmar")

    if pendientes_invitados > 0:
        alertas.append(f"   ⚠️  {pendientes_invitados} personas sin confirmar asistencia")

    if hospedajes_pendientes > 0:
        alertas.append(f"   ⚠️  {hospedajes_pendientes} personas sin hospedaje asignado")

    if not alertas:
        print("   ✅ No hay alertas pendientes")
    else:
        for alerta in alertas:
            print(alerta)

    # Gastos por categoría
    print(f"\n📊 GASTOS POR CATEGORÍA:")
    gastos_categoria = df_presupuesto.groupby('categoria')['valor_total'].sum()
    for categoria, valor in gastos_categoria.items():
        porcentaje = (valor / total_comprometido * 100) if total_comprometido > 0 else 0
        print(f"   {categoria:<12} ${valor:>12,.0f} ({porcentaje:>5.1f}%)")

    print("\n" + "=" * 70)
    print("\n💡 TIP: Para análisis detallado, ejecuta los notebooks en notebooks/")
    print()


if __name__ == "__main__":
    generar_reporte()
