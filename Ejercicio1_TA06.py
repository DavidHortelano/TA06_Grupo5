import os

def detectar_delimitador(linea):
    """Detecta el delimitador en una línea."""
    for delimitador in [',', '\t', ';', ' ']:
        if delimitador in linea:
            return delimitador
    return None

def detectar_tipo(valor):
    """Detecta el tipo de dato de un valor."""
    try:
        int(valor)
        return "int"
    except ValueError:
        try:
            float(valor)
            return "float"
        except ValueError:
            return "str"

def analizar_archivo(ruta_archivo):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            lineas = f.readlines()

        if not lineas:
            print(f"[{ruta_archivo}] El archivo está vacío.")
            return

    
        comentarios = [linea.strip() for linea in lineas if linea.strip().startswith('#')]
        if comentarios:
            print(f"[{ruta_archivo}] Comentarios detectados:")
            for comentario in comentarios:
                print(f"  {comentario}")


        primera_linea = next((linea.strip() for linea in lineas if not linea.strip().startswith('#')), None)
        if not primera_linea:
            print(f"[{ruta_archivo}] No se encontró una cabecera válida.")
            return

  
        delimitador = detectar_delimitador(primera_linea)
        if not delimitador:
            print(f"[{ruta_archivo}] No se detectó un delimitador.")
            return

        print(f"[{ruta_archivo}] Cabecera detectada: {primera_linea}")
        print(f"[{ruta_archivo}] Delimitador detectado: '{delimitador}'")

     
        columnas = primera_linea.split(delimitador)
        datos = [linea.strip().split(delimitador) for linea in lineas if not linea.strip().startswith('#') and delimitador in linea]

        print(f"[{ruta_archivo}] Columnas detectadas: {', '.join(columnas)}")

   
        tipos = []
        for i in range(len(columnas)):
            valores_columna = [fila[i] for fila in datos if len(fila) > i]
            tipos_columna = {detectar_tipo(valor) for valor in valores_columna}
            tipos.append(", ".join(tipos_columna))

        
        print(f"[{ruta_archivo}] Tipos de datos por columna:")
        for col, tipo in zip(columnas, tipos):
            print(f"  - {col}: {tipo}")

    except Exception as e:
        print(f"[{ruta_archivo}] Error: {e}")

def analizar_carpeta(ruta_carpeta):
    if not os.path.isdir(ruta_carpeta):
        print(f"La ruta {ruta_carpeta} no es una carpeta válida.")
        return

    archivos = [os.path.join(ruta_carpeta, archivo) for archivo in os.listdir(ruta_carpeta) if os.path.isfile(os.path.join(ruta_carpeta, archivo))]
    if not archivos:
        print(f"No se encontraron archivos en la carpeta {ruta_carpeta}.")
        return

    print(f"Analizando {len(archivos)} archivos en la carpeta '{ruta_carpeta}':")
    for archivo in archivos:
        print(f"\n--- {archivo} ---")
        analizar_archivo(archivo)

ruta_carpeta = "/workspaces/TA06_Grupo5/prueba" 
analizar_carpeta(ruta_carpeta)
