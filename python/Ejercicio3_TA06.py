import os
import pandas as pd

def limpiar_datos_carpeta(ruta_carpeta):
  
    if not os.path.isdir(ruta_carpeta):
        print(f"La ruta {ruta_carpeta} no es una carpeta válida.")
        return

    archivos = [os.path.join(ruta_carpeta, archivo) for archivo in os.listdir(ruta_carpeta) if archivo.endswith('.dat')]

    if not archivos:
        print(f"No se encontraron archivos .dat en la carpeta {ruta_carpeta}.")
        return

    for archivo in archivos:
        print(f"\nProcesando archivo: {archivo}")
        try:
            df = pd.read_csv(archivo, encoding='utf-8', sep=None, engine='python')
            print("Archivo cargado correctamente.")

            tipos_originales = df.dtypes
            print("Tipos originales de las columnas:")
            print(tipos_originales)

            print("Valores faltantes antes de limpieza:")
            print(df.isnull().sum())

            df = df.fillna(method='ffill').fillna(method='bfill')

            print("Valores faltantes después de limpieza:")
            print(df.isnull().sum())

            archivo_salida = archivo.replace('.dat', '_limpio.dat')
            df.to_csv(archivo_salida, index=False, encoding='utf-8', sep='\t')
            print(f"Archivo limpio guardado como: {archivo_salida}")

        except Exception as e:
            print(f"Error procesando el archivo {archivo}: {e}")

ruta_carpeta = "../prueba"
limpiar_datos_carpeta(ruta_carpeta)
