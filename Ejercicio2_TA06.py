import os

def detectar_formato(archivo):
    """Detecta el número de columnas y el delimitador en la primera línea válida de un archivo."""
    with open(archivo, 'r', encoding='utf-8') as f:
        for linea in f:
            if linea.strip() and not linea.startswith('#'):  # Ignorar líneas vacías o comentarios
                delimitador = next((d for d in [',', '\t', ';', ' '] if d in linea), None)
                if delimitador:
                    columnas = len(linea.split(delimitador))
                    return columnas, delimitador
    return None, None

def verificar_formato_carpeta(carpeta):
    """Verifica si todos los archivos de una carpeta tienen el mismo formato."""
    archivos = [os.path.join(carpeta, f) for f in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, f))]
    formatos = []

    for archivo in archivos:
        columnas, delimitador = detectar_formato(archivo)
        if columnas and delimitador:
            formatos.append((columnas, delimitador))
            print(f"{archivo}: {columnas} columnas, delimitador '{delimitador}'")
        else:
            print(f"{archivo}: No se pudo determinar el formato.")

    if len(set(formatos)) == 1:
        print("\nTodos los archivos tienen el mismo formato.")
    else:
        print("\nLos archivos tienen formatos diferentes.")

ruta_carpeta = "/workspaces/TA06_Grupo5/prueba"
verificar_formato_carpeta(ruta_carpeta)