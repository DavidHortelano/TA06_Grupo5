import os
from collections import Counter

def detectar_formato(archivo):
    """Detecta el formato (número de columnas y delimitador) en las primeras líneas de un archivo."""
    formatos = []
    with open(archivo, 'r', encoding='utf-8') as f:
        for linea in f:
            if linea.strip() and not linea.startswith('#'):
                delimitador = next((d for d in [',', '\t', ';', ' '] if d in linea), None)
                if delimitador:
                    columnas = len(linea.split(delimitador))
                    formatos.append((columnas, delimitador))
    return formatos

def calcular_estadisticas(formatos_globales):
    """Calcula estadísticas sobre los formatos detectados."""
    contador_columnas = Counter([formato[0] for formato in formatos_globales.values()])
    contador_delimitadores = Counter([formato[1] for formato in formatos_globales.values()])
    
    print("\nResumen estadístico:")
    print("- Distribución del número de columnas:")
    for columnas, cantidad in contador_columnas.items():
        print(f"  {columnas} columnas: {cantidad} archivos")
    
    print("- Distribución de delimitadores:")
    for delimitador, cantidad in contador_delimitadores.items():
        print(f"  '{delimitador}' utilizado en {cantidad} archivos")

def analizar_archivos_en_carpeta(carpeta):
    """Analiza los archivos en una carpeta y genera un resumen estadístico."""
    archivos = [os.path.join(carpeta, f) for f in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, f))]
    formatos_globales = {}

    for archivo in archivos:
        formatos = detectar_formato(archivo)
        if formatos:
            formatos_globales[archivo] = formatos[0] 
            print(f"{archivo}: {formatos[0][0]} columnas, delimitador '{formatos[0][1]}'")
        else:
            print(f"{archivo}: No se pudo determinar el formato.")
    
    calcular_estadisticas(formatos_globales)


ruta_carpeta = "/workspaces/TA06_Grupo5/prueba" 
analizar_archivos_en_carpeta(ruta_carpeta)
