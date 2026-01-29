#!/usr/bin/env python3
"""
Sistema de alertas para el matrimonio.
Monitorea presupuesto, fechas límite y confirmaciones.
Uso: python scripts/alertas.py
"""

import pandas as pd
import sys
from pathlib import Path
from datetime import datetime, timedelta

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


def alerta_presupuesto(df):
    """Verifica alertas relacionadas con el presupuesto."""
    alertas = []

    total_comprometido = df['valor_total'].sum()
    porcentaje_usado = (total_comprometido / PRESUPUESTO_TOTAL) * 100

    # Alerta crítica: >90%
    if porcentaje_usado > 90:
        alertas.append({
            'nivel': 'CRÍTICO',
            'emoji': '🔴',
            'titulo': 'Presupuesto en nivel crítico',
            'mensaje': f'Has usado {porcentaje_usado:.1f}% del presupuesto total. '
                      f'Disponible: ${PRESUPUESTO_TOTAL - total_comprometido:,.0f}',
            'accion': 'Revisa gastos urgentemente o considera aumentar presupuesto'
        })
    # Alerta advertencia: >70%
    elif porcentaje_usado > 70:
        alertas.append({
            'nivel': 'ADVERTENCIA',
            'emoji': '🟡',
            'titulo': 'Presupuesto en precaución',
            'mensaje': f'Has usado {porcentaje_usado:.1f}% del presupuesto. '
                      f'Disponible: ${PRESUPUESTO_TOTAL - total_comprometido:,.0f}',
            'accion': 'Monitorea cuidadosamente los gastos restantes'
        })

    # Alerta: items sin confirmar
    sin_confirmar = df[df['confirmado'] == False]
    if len(sin_confirmar) > 0:
        valor_sin_confirmar = sin_confirmar['valor_total'].sum()
        alertas.append({
            'nivel': 'ADVERTENCIA',
            'emoji': '⚠️',
            'titulo': 'Ítems de presupuesto sin confirmar',
            'mensaje': f'{len(sin_confirmar)} ítems sin confirmar '
                      f'(${valor_sin_confirmar:,.0f} comprometidos)',
            'accion': f'Confirmar servicios: {", ".join(sin_confirmar["item"].head(5).tolist())}'
                     + ('...' if len(sin_confirmar) > 5 else '')
        })

    return alertas


def alerta_fechas(df):
    """Verifica alertas relacionadas con fechas límite."""
    alertas = []

    # Convertir fechas
    df['fecha_limite'] = pd.to_datetime(df['fecha_limite'], errors='coerce')

    hoy = datetime.now()
    fecha_30_dias = hoy + timedelta(days=30)
    fecha_15_dias = hoy + timedelta(days=15)

    # Items con fecha límite en los próximos 30 días sin confirmar
    proximos_30 = df[
        (df['fecha_limite'] <= fecha_30_dias) &
        (df['fecha_limite'] > hoy) &
        (df['confirmado'] == False)
    ]

    if len(proximos_30) > 0:
        # Separar por urgencia
        proximos_15 = proximos_30[proximos_30['fecha_limite'] <= fecha_15_dias]

        if len(proximos_15) > 0:
            alertas.append({
                'nivel': 'URGENTE',
                'emoji': '🔴',
                'titulo': 'Fechas límite URGENTES',
                'mensaje': f'{len(proximos_15)} ítems con fecha límite en los próximos 15 días',
                'accion': 'Confirmar inmediatamente: ' +
                         ', '.join([f"{row['item']} ({row['fecha_limite'].strftime('%Y-%m-%d')})"
                                   for _, row in proximos_15.iterrows()])
            })

        proximos_30_no_urgentes = proximos_30[proximos_30['fecha_limite'] > fecha_15_dias]
        if len(proximos_30_no_urgentes) > 0:
            alertas.append({
                'nivel': 'ADVERTENCIA',
                'emoji': '🟡',
                'titulo': 'Fechas límite próximas',
                'mensaje': f'{len(proximos_30_no_urgentes)} ítems con fecha límite en 15-30 días',
                'accion': 'Planificar confirmación: ' +
                         ', '.join([f"{row['item']} ({row['fecha_limite'].strftime('%Y-%m-%d')})"
                                   for _, row in proximos_30_no_urgentes.head(3).iterrows()])
            })

    # Items con fecha límite vencida
    vencidos = df[(df['fecha_limite'] < hoy) & (df['confirmado'] == False)]
    if len(vencidos) > 0:
        alertas.append({
            'nivel': 'CRÍTICO',
            'emoji': '🔴',
            'titulo': 'Fechas límite VENCIDAS',
            'mensaje': f'{len(vencidos)} ítems con fecha límite vencida',
            'accion': 'ACCIÓN INMEDIATA: ' +
                     ', '.join([f"{row['item']}" for _, row in vencidos.iterrows()])
        })

    return alertas


def alerta_invitados(df):
    """Verifica alertas relacionadas con invitados."""
    alertas = []

    # Invitados sin confirmar
    sin_confirmar = df[df['confirmado'] == False]
    total_sin_confirmar = sin_confirmar['personas'].sum()

    if len(sin_confirmar) > 0:
        porcentaje_sin_confirmar = (total_sin_confirmar / df['personas'].sum()) * 100

        nivel = 'CRÍTICO' if porcentaje_sin_confirmar > 50 else 'ADVERTENCIA'
        emoji = '🔴' if porcentaje_sin_confirmar > 50 else '🟡'

        alertas.append({
            'nivel': nivel,
            'emoji': emoji,
            'titulo': 'Invitados sin confirmar',
            'mensaje': f'{len(sin_confirmar)} grupos ({total_sin_confirmar} personas, '
                      f'{porcentaje_sin_confirmar:.1f}%) sin confirmar asistencia',
            'accion': 'Contactar grupos: ' +
                     ', '.join(sin_confirmar['nombre'].head(5).tolist()) +
                     ('...' if len(sin_confirmar) > 5 else '')
        })

    return alertas


def alerta_hospedaje(df_hospedaje, df_invitados):
    """Verifica alertas relacionadas con hospedaje."""
    alertas = []

    # Hospedajes sin asignar
    sin_asignar = df_hospedaje[df_hospedaje['asignado'] == False]
    total_sin_asignar = sin_asignar['personas_hospedaje'].sum()

    if len(sin_asignar) > 0:
        porcentaje_sin_asignar = (total_sin_asignar / df_hospedaje['personas_hospedaje'].sum()) * 100

        nivel = 'CRÍTICO' if porcentaje_sin_asignar > 50 else 'ADVERTENCIA'
        emoji = '🔴' if porcentaje_sin_asignar > 50 else '🟡'

        alertas.append({
            'nivel': nivel,
            'emoji': emoji,
            'titulo': 'Hospedajes sin asignar',
            'mensaje': f'{len(sin_asignar)} grupos ({total_sin_asignar} personas, '
                      f'{porcentaje_sin_asignar:.1f}%) sin hospedaje asignado',
            'accion': 'Asignar hospedaje: ' +
                     ', '.join(sin_asignar['nombre_invitado'].head(5).tolist()) +
                     ('...' if len(sin_asignar) > 5 else '')
        })

    # Invitados con hospedaje confirmado pero sin asignar habitación
    confirmados_hospedaje = df_invitados[
        (df_invitados['hospedaje'] > 0) &
        (df_invitados['confirmado'] == True)
    ]

    for _, inv in confirmados_hospedaje.iterrows():
        hosp = df_hospedaje[df_hospedaje['nombre_invitado'] == inv['nombre']]
        if len(hosp) > 0 and not hosp.iloc[0]['asignado']:
            alertas.append({
                'nivel': 'ADVERTENCIA',
                'emoji': '⚠️',
                'titulo': 'Invitado confirmado sin hospedaje',
                'mensaje': f"{inv['nombre']} confirmó asistencia pero no tiene habitación asignada",
                'accion': f'Asignar habitación urgente para {inv["hospedaje"]} persona(s)'
            })

    return alertas


def imprimir_alertas(todas_alertas):
    """Imprime todas las alertas de forma organizada."""
    print("\n" + "=" * 70)
    print(" " * 20 + "SISTEMA DE ALERTAS")
    print("=" * 70)

    if not todas_alertas:
        print("\n✅ ¡Excelente! No hay alertas pendientes.")
        print("   Todo está bajo control.\n")
        return

    # Organizar por nivel
    criticas = [a for a in todas_alertas if a['nivel'] == 'CRÍTICO']
    urgentes = [a for a in todas_alertas if a['nivel'] == 'URGENTE']
    advertencias = [a for a in todas_alertas if a['nivel'] == 'ADVERTENCIA']

    # Mostrar alertas críticas
    if criticas:
        print(f"\n🔴 ALERTAS CRÍTICAS ({len(criticas)}):")
        print("=" * 70)
        for i, alerta in enumerate(criticas, 1):
            print(f"\n{i}. {alerta['titulo']}")
            print(f"   {alerta['mensaje']}")
            print(f"   → {alerta['accion']}")

    # Mostrar alertas urgentes
    if urgentes:
        print(f"\n⚠️  ALERTAS URGENTES ({len(urgentes)}):")
        print("=" * 70)
        for i, alerta in enumerate(urgentes, 1):
            print(f"\n{i}. {alerta['titulo']}")
            print(f"   {alerta['mensaje']}")
            print(f"   → {alerta['accion']}")

    # Mostrar advertencias
    if advertencias:
        print(f"\n🟡 ADVERTENCIAS ({len(advertencias)}):")
        print("=" * 70)
        for i, alerta in enumerate(advertencias, 1):
            print(f"\n{i}. {alerta['titulo']}")
            print(f"   {alerta['mensaje']}")
            print(f"   → {alerta['accion']}")

    # Resumen
    print("\n" + "=" * 70)
    print(f"RESUMEN: {len(criticas)} críticas, {len(urgentes)} urgentes, "
          f"{len(advertencias)} advertencias")
    print("=" * 70 + "\n")


def main():
    """Ejecuta el sistema de alertas."""
    df_presupuesto, df_invitados, df_hospedaje = cargar_datos()

    # Recolectar todas las alertas
    todas_alertas = []
    todas_alertas.extend(alerta_presupuesto(df_presupuesto))
    todas_alertas.extend(alerta_fechas(df_presupuesto))
    todas_alertas.extend(alerta_invitados(df_invitados))
    todas_alertas.extend(alerta_hospedaje(df_hospedaje, df_invitados))

    # Imprimir alertas
    imprimir_alertas(todas_alertas)


if __name__ == "__main__":
    main()
