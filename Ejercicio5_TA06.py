import os
import pandas as pd
import matplotlib.pyplot as plt

def analizar_datos_documentado(ruta_carpeta):
    if not os.path.isdir(ruta_carpeta):
        print(f"La ruta {ruta_carpeta} no es una carpeta válida.")
        return

    archivos = [os.path.join(ruta_carpeta, archivo) for archivo in os.listdir(ruta_carpeta) if archivo.endswith('.dat')]

    if not archivos:
        print(f"No se encontraron archivos .dat en la carpeta {ruta_carpeta}.")
        return

    total_valores_procesados = 0
    resumen_estadistico = []

    for archivo in archivos:
        print(f"\nProcesando archivo: {archivo}")
        try:
            df = pd.read_csv(archivo, encoding='utf-8', sep='\t', engine='python')
            df.replace(-999, pd.NA, inplace=True)
            df.fillna(df.mean(numeric_only=True), inplace=True)

            if 'Precipitacion' in df.columns and 'Anyo' in df.columns:
                totales_anuales = df.groupby('Anyo')['Precipitacion'].sum()
                medias_anuales = df.groupby('Anyo')['Precipitacion'].mean()
                tasa_variacion = totales_anuales.pct_change() * 100

                max_precipitacion = totales_anuales.idxmax()
                min_precipitacion = totales_anuales.idxmin()

                resumen_estadistico.append({
                    "Archivo": os.path.basename(archivo),
                    "Año más lluvioso": max_precipitacion,
                    "Precipitación máxima (mm)": totales_anuales[max_precipitacion],
                    "Año más seco": min_precipitacion,
                    "Precipitación mínima (mm)": totales_anuales[min_precipitacion],
                    "Máxima variación interanual (%)": tasa_variacion.abs().max()
                })

                total_valores_procesados += df.size

                # Generar gráfico
                plt.figure(figsize=(10, 5))
                plt.bar(totales_anuales.index, totales_anuales.values, color='blue')
                plt.xlabel('Año')
                plt.ylabel('Precipitación Total (mm)')
                plt.title(f'Precipitación Total por Año ({os.path.basename(archivo)})')
                plt.xticks(rotation=45)
                plt.grid(axis='y', linestyle='--', alpha=0.7)
                plt.show()
        
        except Exception as e:
            print(f"Error procesando el archivo {archivo}: {e}")

    # Guardar el resumen en un CSV
    if resumen_estadistico:
        df_resumen = pd.DataFrame(resumen_estadistico)
        df_resumen.to_csv(os.path.join(ruta_carpeta, "resumen_estadistico.csv"), index=False, encoding='utf-8')
        print(f"Resumen estadístico guardado en {os.path.join(ruta_carpeta, 'resumen_estadistico.csv')}")

    print(f"\nTotal de valores procesados en todos los archivos: {total_valores_procesados}")

# Ejecutar la función
ruta_carpeta = "/workspaces/TA06_Grupo5/prueba"
analizar_datos_documentado(ruta_carpeta)
