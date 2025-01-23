import os
import pandas as pd

def analizar_datos_documentado(ruta_carpeta):
    
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
            df = pd.read_csv(archivo, encoding='utf-8', sep='\t', engine='python')

            print("\n=== Documentación del proceso ===")
            print("1. Los valores '-999' se consideran datos faltantes y se reemplazan por NaN.")
            print("2. Los valores nulos se rellenan usando la media de la columna correspondiente.")

            df.replace(-999, pd.NA, inplace=True)

            porcentaje_faltantes = df.isna().mean() * 100
            porcentaje_no_faltantes = 100 - porcentaje_faltantes

            print("\nPorcentaje de datos faltantes por columna:")
            print(porcentaje_faltantes)

            print("\nPorcentaje de datos no faltantes por columna:")
            print(porcentaje_no_faltantes)

            df.fillna(df.mean(numeric_only=True), inplace=True)

            print("\n=== Estadísticas Generales ===")
            if 'Precipitacion' in df.columns and 'Anyo' in df.columns:
                totales_anuales = df.groupby('Anyo')['Precipitacion'].sum()
                medias_anuales = df.groupby('Anyo')['Precipitacion'].mean()

                print("Precipitación total por año:")
                print(totales_anuales)
                print("\nPrecipitación media por año:")
                print(medias_anuales)

                tasa_variacion = totales_anuales.pct_change() * 100
                print("\nTasa de variación anual (%):")
                print(tasa_variacion)

                max_precipitacion = totales_anuales.idxmax()
                min_precipitacion = totales_anuales.idxmin()

                print(f"\nEl año más lluvioso fue {max_precipitacion} con {totales_anuales[max_precipitacion]} mm.")
                print(f"El año más seco fue {min_precipitacion} con {totales_anuales[min_precipitacion]} mm.")

                print("\n=== Estadísticas Adicionales ===")

                media_global = df['Precipitacion'].mean()
                sequias = (totales_anuales < media_global).astype(int).groupby((totales_anuales >= media_global).astype(int).cumsum()).sum()
                print("Duración de sequías (años consecutivos con precipitaciones por debajo de la media):")
                print(sequias)

                max_variacion = tasa_variacion.abs().max()
                print(f"\nMáxima variación interanual: {max_variacion:.2f}%")

        except Exception as e:
            print(f"Error procesando el archivo {archivo}: {e}")

ruta_carpeta = "/workspaces/TA06_Grupo5/prueba"
analizar_datos_documentado(ruta_carpeta)
