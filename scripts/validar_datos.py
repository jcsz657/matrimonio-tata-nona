#!/usr/bin/env python3
"""
Script para validar la integridad de los datos del matrimonio.
Uso: python scripts/validar_datos.py
"""

import pandas as pd
import sys
from pathlib import Path
from datetime import datetime

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


def validar_presupuesto(df):
    """Valida los datos de presupuesto."""
    errores = []
    advertencias = []

    print("\n🔍 Validando presupuesto...")

    # 1. Validar que saldo = valor_total - abonado
    for idx, row in df.iterrows():
        if row['valor_total'] > 0:
            saldo_calculado = row['valor_total'] - row['abonado']
            if abs(row['saldo'] - saldo_calculado) > 0.01:  # Tolerancia para redondeo
                errores.append(
                    f"   ❌ Fila {idx+2}: {row['item']} - "
                    f"Saldo incorrecto (esperado: ${saldo_calculado:,.0f}, "
                    f"actual: ${row['saldo']:,.0f})"
                )

    # 2. Validar que no hay valores negativos
    for col in ['valor_total', 'abonado', 'saldo']:
        negativos = df[df[col] < 0]
        if len(negativos) > 0:
            for idx, row in negativos.iterrows():
                errores.append(
                    f"   ❌ Fila {idx+2}: {row['item']} - "
                    f"{col} no puede ser negativo (${row[col]:,.0f})"
                )

    # 3. Validar que abonado <= valor_total
    sobrepago = df[df['abonado'] > df['valor_total']]
    if len(sobrepago) > 0:
        for idx, row in sobrepago.iterrows():
            errores.append(
                f"   ❌ Fila {idx+2}: {row['item']} - "
                f"Abonado (${row['abonado']:,.0f}) excede valor total (${row['valor_total']:,.0f})"
            )

    # 4. Validar fechas
    df['fecha_limite'] = pd.to_datetime(df['fecha_limite'], errors='coerce')
    fechas_invalidas = df[df['fecha_limite'].isna() & df['fecha_limite'].notna()]
    if len(fechas_invalidas) > 0:
        for idx, row in fechas_invalidas.iterrows():
            advertencias.append(
                f"   ⚠️  Fila {idx+2}: {row['item']} - Fecha límite inválida"
            )

    # 5. Advertir si el presupuesto total excede el límite
    total_comprometido = df['valor_total'].sum()
    if total_comprometido > PRESUPUESTO_TOTAL:
        diferencia = total_comprometido - PRESUPUESTO_TOTAL
        errores.append(
            f"   ❌ El presupuesto total (${total_comprometido:,.0f}) "
            f"excede el límite (${PRESUPUESTO_TOTAL:,}) por ${diferencia:,.0f}"
        )

    # 6. Advertir sobre items sin cotizar
    sin_cotizar = df[(df['valor_total'] == 0) & (df['confirmado'] == False)]
    if len(sin_cotizar) > 0:
        advertencias.append(
            f"   ⚠️  {len(sin_cotizar)} ítems sin cotizar: "
            f"{', '.join(sin_cotizar['item'].tolist())}"
        )

    return errores, advertencias


def validar_invitados(df):
    """Valida los datos de invitados."""
    errores = []
    advertencias = []

    print("\n🔍 Validando invitados...")

    # 1. Validar que hospedaje <= personas
    exceso_hospedaje = df[df['hospedaje'] > df['personas']]
    if len(exceso_hospedaje) > 0:
        for idx, row in exceso_hospedaje.iterrows():
            errores.append(
                f"   ❌ Fila {idx+2}: {row['nombre']} - "
                f"Hospedaje ({row['hospedaje']}) no puede ser mayor que personas ({row['personas']})"
            )

    # 2. Validar que personas y hospedaje no sean negativos
    for col in ['personas', 'hospedaje']:
        negativos = df[df[col] < 0]
        if len(negativos) > 0:
            for idx, row in negativos.iterrows():
                errores.append(
                    f"   ❌ Fila {idx+2}: {row['nombre']} - "
                    f"{col} no puede ser negativo ({row[col]})"
                )

    # 3. Validar grupos válidos
    grupos_validos = ['PUENTE', 'BOGOTA', 'CASA']
    grupos_invalidos = df[~df['grupo'].isin(grupos_validos)]
    if len(grupos_invalidos) > 0:
        for idx, row in grupos_invalidos.iterrows():
            errores.append(
                f"   ❌ Fila {idx+2}: {row['nombre']} - "
                f"Grupo inválido '{row['grupo']}' (debe ser: {', '.join(grupos_validos)})"
            )

    # 4. Advertir sobre pendientes de confirmar
    pendientes = df[df['confirmado'] == False]
    if len(pendientes) > 0:
        total_personas = pendientes['personas'].sum()
        advertencias.append(
            f"   ⚠️  {len(pendientes)} grupos ({total_personas} personas) sin confirmar"
        )

    return errores, advertencias


def validar_hospedaje(df_hospedaje, df_invitados):
    """Valida los datos de hospedaje."""
    errores = []
    advertencias = []

    print("\n🔍 Validando hospedaje...")

    # 1. Validar que no hay valores negativos
    for col in ['personas_hospedaje', 'costo_estimado']:
        negativos = df_hospedaje[df_hospedaje[col] < 0]
        if len(negativos) > 0:
            for idx, row in negativos.iterrows():
                errores.append(
                    f"   ❌ Fila {idx+2}: {row['nombre_invitado']} - "
                    f"{col} no puede ser negativo ({row[col]})"
                )

    # 2. Verificar que todos los invitados con hospedaje están en la lista
    invitados_con_hospedaje = df_invitados[df_invitados['hospedaje'] > 0]['nombre'].tolist()
    nombres_hospedaje = df_hospedaje['nombre_invitado'].tolist()

    # Verificar que las personas en hospedaje coincidan
    for _, row_inv in df_invitados[df_invitados['hospedaje'] > 0].iterrows():
        row_hosp = df_hospedaje[df_hospedaje['nombre_invitado'] == row_inv['nombre']]
        if len(row_hosp) == 0:
            advertencias.append(
                f"   ⚠️  {row_inv['nombre']} tiene hospedaje en invitados.csv "
                f"pero no está en hospedaje.csv"
            )
        elif row_hosp.iloc[0]['personas_hospedaje'] != row_inv['hospedaje']:
            advertencias.append(
                f"   ⚠️  {row_inv['nombre']}: "
                f"Discrepancia en personas de hospedaje "
                f"(invitados: {row_inv['hospedaje']}, hospedaje: {row_hosp.iloc[0]['personas_hospedaje']})"
            )

    # 3. Advertir sobre hospedajes sin asignar
    sin_asignar = df_hospedaje[df_hospedaje['asignado'] == False]
    if len(sin_asignar) > 0:
        total_personas = sin_asignar['personas_hospedaje'].sum()
        advertencias.append(
            f"   ⚠️  {len(sin_asignar)} hospedajes sin asignar ({total_personas} personas)"
        )

    return errores, advertencias


def main():
    """Ejecuta todas las validaciones."""
    print("\n" + "=" * 70)
    print(" " * 20 + "VALIDACIÓN DE DATOS")
    print("=" * 70)

    df_presupuesto, df_invitados, df_hospedaje = cargar_datos()

    # Validar cada conjunto de datos
    errores_presupuesto, advertencias_presupuesto = validar_presupuesto(df_presupuesto)
    errores_invitados, advertencias_invitados = validar_invitados(df_invitados)
    errores_hospedaje, advertencias_hospedaje = validar_hospedaje(df_hospedaje, df_invitados)

    # Consolidar resultados
    todos_errores = errores_presupuesto + errores_invitados + errores_hospedaje
    todas_advertencias = advertencias_presupuesto + advertencias_invitados + advertencias_hospedaje

    # Mostrar resultados
    print("\n" + "=" * 70)
    print("RESULTADOS:")
    print("=" * 70)

    if todos_errores:
        print(f"\n❌ ERRORES ENCONTRADOS ({len(todos_errores)}):\n")
        for error in todos_errores:
            print(error)

    if todas_advertencias:
        print(f"\n⚠️  ADVERTENCIAS ({len(todas_advertencias)}):\n")
        for advertencia in todas_advertencias:
            print(advertencia)

    if not todos_errores and not todas_advertencias:
        print("\n✅ ¡Excelente! Todos los datos son válidos y consistentes.")
    elif not todos_errores:
        print("\n✅ No se encontraron errores críticos.")
        print("⚠️  Revisa las advertencias para mejorar la calidad de los datos.")
    else:
        print(f"\n❌ Se encontraron {len(todos_errores)} errores que deben corregirse.")
        sys.exit(1)

    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()
