import pandas as pd

# ============================================================
# Diccionario: ruta del archivo → nombre del indicador
# ============================================================
archivos = {
    'data\\PoblacionMatriculada.xlsx': 'Poblacion Matriculada',
    'data\\TasaEfectivos.xlsx':        'Tasa Efectivos',
    'data\\TasaPromovidos.xlsx':       'Tasa Promovidos',
    'data\\TasaReprobados.xlsx':       'Tasa Reprobados',
    'data\\TasaAbandono.xlsx':         'Tasa Abandono',
}

# ============================================================
# Función de limpieza (tu código convertido en función)
# ============================================================
def limpiar_tipo_a(ruta, indicador):

    df_raw = pd.read_excel(ruta, header=None)

    # Rellenar años (fila 10) hacia adelante
    row_years  = df_raw.iloc[10, :].tolist()
    row_gender = df_raw.iloc[11, :].tolist()

    years_fill = []
    last = None
    for v in row_years:
        if pd.notnull(v):
            last = v
        years_fill.append(last)

    # Construir nombres de columna
    name_columns = []
    for i, (year, gender) in enumerate(zip(years_fill, row_gender)):
        if i == 0:
            name_columns.append("_index")
        elif i == 1:
            name_columns.append("category")
        elif pd.notna(gender) and pd.notna(year):
            name_columns.append(f"{int(year)}_{gender}")
        else:
            name_columns.append(f"col{i}")

    # Extraer y limpiar filas de datos
    df = df_raw.iloc[13:].copy()
    df.columns = name_columns
    df = df.drop(columns=["_index"])
    df = df[df["category"].notna()].copy()
    df = df[~df["category"].str.contains("Ministerio|Instituto|Fuente", na=False)]
    df = df.reset_index(drop=True)

    # Convertir a formato largo
    df_long = df.melt(id_vars=["category"], var_name="year_gender", value_name="value")
    df_long[["year", "gender"]] = df_long["year_gender"].str.split("_", expand=True)
    df_long = df_long.drop(columns=["year_gender"])
    df_long["year"]     = pd.to_numeric(df_long["year"],  errors="coerce")
    df_long["value"]    = pd.to_numeric(df_long["value"], errors="coerce")
    df_long             = df_long.dropna(subset=["value"]).copy()
    df_long["category"] = df_long["category"].str.strip()

    # Asignar indicador automáticamente según el archivo
    df_long["indicator"] = indicador

    print(f"✓ {indicador}: {df_long.shape[0]} filas | años {int(df_long['year'].min())}–{int(df_long['year'].max())}")
    return df_long

# ============================================================
# Procesar todos los archivos y unirlos
# ============================================================
dfs = []
for ruta, indicador in archivos.items():
    df_limpio = limpiar_tipo_a(ruta, indicador)
    dfs.append(df_limpio)

todos = pd.concat(dfs, ignore_index=True)
todos.to_csv("educacion_bolivia_limpio.csv", index=False)

print(f"\nArchivo guardado: {todos.shape[0]} filas · {todos.shape[1]} columnas")
print(f"Indicadores incluidos: {todos['indicator'].unique()}")

# Lista de departamentos reales de Bolivia
departamentos = [
    "BOLIVIA", "Chuquisaca", "La Paz", "Cochabamba",
    "Oruro", "Potosí", "Tarija", "Santa Cruz", "Beni", "Pando"
]

# Función que recorre el DataFrame y asigna departamento a cada fila
def asignar_departamento(df):
    df = df.copy()
    df["department"] = None        # nueva columna
    df["dependency"] = None        # nueva columna

    depto_actual = None

    for idx, row in df.iterrows():
        cat = row["category"].strip()

        if cat.upper() in [d.upper() for d in departamentos]:
            # Es una fila de departamento (o Bolivia total)
            depto_actual = cat
            df.at[idx, "department"] = cat
            df.at[idx, "dependency"] = "Total"
        else:
            # Es Público o Privado — hereda el departamento anterior
            df.at[idx, "department"] = depto_actual
            df.at[idx, "dependency"] = cat

    return df

todos = asignar_departamento(todos)

# Eliminar la columna category (ya no la necesitamos)
todos = todos.drop(columns=["category"])

# Reordenar columnas de forma lógica
todos = todos[["department", "dependency", "year", "gender", "indicator", "value"]]

print(todos.head(20).to_string())
print(f"\nDepartamentos: {sorted(todos['department'].unique())}")
print(f"Dependencias: {todos['dependency'].unique()}")

# Verificación rápida: ¿cada fila tiene departamento asignado?
print("Filas sin departamento:", todos["department"].isna().sum())
print("Filas sin dependencia:", todos["dependency"].isna().sum())

# Ver un resumen por indicador y dependencia
print(todos.groupby(["indicator", "dependency"])["value"].count())

# Definir qué valores corresponden a cada dimensión
sectores = ["Total", "Público", "Privado"]
niveles  = ["INICIAL", "PRIMARIA", "SECUNDARIA"]

# Crear dos columnas separadas
todos["sector"] = todos["dependency"].where(todos["dependency"].isin(sectores), other="Total")
todos["nivel"]  = todos["dependency"].where(todos["dependency"].isin(niveles),  other="Total")

# Eliminar la columna original ya que está separada
todos = todos.drop(columns=["dependency"])

# Reordenar columnas
todos = todos[["department", "sector", "nivel", "year", "gender", "indicator", "value"]]

# Verificar
print(todos["sector"].unique())
print(todos["nivel"].unique())
print(todos.head(10).to_string())



# Guardar versión final limpia
todos.to_csv("educacion_bolivia_limpio.csv", index=False)
print("\n✓ Archivo guardado correctamente")