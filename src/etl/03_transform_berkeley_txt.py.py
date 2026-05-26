import pandas as pd
import knime.scripting.io as knio
import os
import ast
from urllib.parse import urlparse, unquote

tabla = knio.input_tables[0].to_pandas()
ruta_original = tabla["Path"].iloc[0]

ANIO_INICIO = 1990
ANIO_FIN = 2015

def obtener_ruta_real(valor):
    # Caso 1: ya viene como dict
    if isinstance(valor, dict):
        return valor.get("path", "")
    
    # Caso 2: viene como string que representa un dict
    texto = str(valor).strip()
    if texto.startswith("{") and "'path'" in texto:
        try:
            obj = ast.literal_eval(texto)
            if isinstance(obj, dict):
                return obj.get("path", texto)
        except:
            pass
    
    # Caso 3: ya viene como ruta normal
    return texto

def normalizar_ruta(ruta):
    ruta = str(ruta).strip()
    if ruta.startswith("file:/"):
        parsed = urlparse(ruta)
        ruta = unquote(parsed.path)
        if len(ruta) > 2 and ruta[0] == "/" and ruta[2] == ":":
            ruta = ruta[1:]
    return ruta

def extraer_pais(lineas):
    for linea in lineas:
        limpio = linea.strip()
        if limpio.startswith("%%") and "Name:" in limpio:
            return limpio.split("Name:", 1)[1].strip()
    return None

def extraer_base_mensual(lineas):
    for linea in lineas:
        limpio = linea.strip()
        if limpio.startswith("%%"):
            partes = limpio.split()
            if len(partes) == 13:
                try:
                    valores = list(map(float, partes[1:]))
                    return {i + 1: v for i, v in enumerate(valores)}
                except:
                    continue
    return None

resultado = []

try:
    ruta_real = obtener_ruta_real(ruta_original)
    ruta = normalizar_ruta(ruta_real)
    nombre_archivo = os.path.basename(ruta)

    print("Valor original Path:", ruta_original)
    print("Ruta real:", ruta)

    with open(ruta, "r", encoding="utf8") as f:
        lineas = f.readlines()

    pais = extraer_pais(lineas)
    if pais is None:
        pais = nombre_archivo.replace("-TAVG-Trend.txt", "").replace(".txt", "").replace("-", " ").title()

    base = extraer_base_mensual(lineas)

    for linea in lineas:
        linea = linea.strip()

        if not linea or linea.startswith("%"):
            continue

        partes = linea.split()
        if len(partes) < 4:
            continue

        try:
            year = int(partes[0])
            month = int(partes[1])

            # FILTRO DE AÑOS
            if year < ANIO_INICIO or year > ANIO_FIN:
                continue

            anomaly = None if partes[2] == "NaN" else float(partes[2])
            unc = None if partes[3] == "NaN" else float(partes[3])

            temp_abs = None
            if anomaly is not None and base is not None and month in base:
                temp_abs = anomaly + base[month]

            resultado.append({
                "Country": pais,
                "Year": year,
                "Month": month,
                "Anomaly_temp": anomaly,
                "Unc_temp": unc,
                "Abs_temperature_c": temp_abs,
            })

        except Exception as e:
            print(f"Error en línea '{linea}': {e}")

except Exception as e:
    print(f"Error procesando archivo {ruta_original}: {e}")

df = pd.DataFrame(resultado)

if not df.empty:
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
    df["Month"] = pd.to_numeric(df["Month"], errors="coerce").astype("Int64")
    df["Anomaly_temp"] = pd.to_numeric(df["Anomaly_temp"], errors="coerce")
    df["Unc_temp"] = pd.to_numeric(df["Unc_temp"], errors="coerce")
    df["Abs_temperature_c"] = pd.to_numeric(df["Abs_temperature_c"], errors="coerce")

knio.output_tables[0] = knio.Table.from_pandas(df)
