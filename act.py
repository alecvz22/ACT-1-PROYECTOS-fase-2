import os
import re
import time

# Carpeta donde están los archivos HTML
carpeta_html = "./Files 2"

# Archivos de salida
log_file = "act3.txt"
archivo_global = "palabras.txt"
palabra_a_buscar = "corel".lower()  # palabra que quieras buscar

def remover_etiquetas_html(nombre_archivo):
    ruta = os.path.join(carpeta_html, nombre_archivo)
    # Abrir con encoding latin-1 para evitar errores de codificación
    with open(ruta, "r", encoding="latin-1") as f:
        contenido = f.read()
    # Eliminar todas las etiquetas HTML
    contenido_limpio = re.sub(r"<[^>]+>", " ", contenido)
    return contenido_limpio

def extraer_palabras(texto):
    # Solo letras, minúsculas, sin números ni símbolos
    palabras = re.findall(r"\b[a-zA-Z]+\b", texto)
    return set([p.lower() for p in palabras])

def main():
    todas_las_palabras = set()
    archivos_por_palabra = {}  # palabra -> lista de archivos

    with open(log_file, "w", encoding="utf-8") as log:
        log.write("Medición de tiempos - Procesamiento global de palabras únicas (solo letras)\n")
        log.write("----------------------------------------------------------------\n\n")

        tiempo_inicio_total = time.time()

        for archivo in os.listdir(carpeta_html):
            if archivo.endswith(".html"):
                inicio = time.time()
                texto_limpio = remover_etiquetas_html(archivo)
                palabras = extraer_palabras(texto_limpio)
                fin = time.time()
                tiempo_archivo = fin - inicio

                todas_las_palabras.update(palabras)
                log.write(f"{archivo}: {tiempo_archivo:.6f} segundos\n")

                # Guardar en qué archivo aparece cada palabra
                for p in palabras:
                    if p not in archivos_por_palabra:
                        archivos_por_palabra[p] = []
                    archivos_por_palabra[p].append(archivo)

        lista_ordenada = sorted(todas_las_palabras)

        # Guardar palabras únicas en archivo global
        with open(archivo_global, "w", encoding="utf-8") as f:
            for palabra in lista_ordenada:
                f.write(palabra + "\n")

        tiempo_fin_total = time.time()
        tiempo_total = tiempo_fin_total - tiempo_inicio_total
        log.write("\n----------------------------------------------------------------\n")
        log.write(f"Tiempo total en procesar todos los archivos: {tiempo_total:.6f} segundos\n")

    # Buscar palabra en los archivos
    if palabra_a_buscar in archivos_por_palabra:
        print(f"✔ La palabra '{palabra_a_buscar}' aparece en los siguientes archivos:")
        for archivo in archivos_por_palabra[palabra_a_buscar]:
            print(f"  - {archivo}")
    else:
        print(f"✘ La palabra '{palabra_a_buscar}' no aparece en ningún archivo.")

if __name__ == "__main__":
    main()
