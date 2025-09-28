import os
import re
import sys
import time
from collections import Counter, defaultdict

def remover_etiquetas_html(ruta_archivo):
    """Elimina etiquetas HTML y devuelve el texto limpio"""
    with open(ruta_archivo, "r", encoding="latin-1") as f:
        contenido = f.read()
    return re.sub(r"<[^>]+>", " ", contenido)

def extraer_palabras(texto):
    """Extrae palabras (solo letras) y las convierte a minúsculas"""
    return [p.lower() for p in re.findall(r"\b[a-zA-Z]+\b", texto)]

def main():
    if len(sys.argv) != 3:
        print("Uso: python3 act6.py <input-directory> <output-directory>")
        sys.exit(1)

    carpeta_html = sys.argv[1]
    carpeta_salida = sys.argv[2]
    os.makedirs(carpeta_salida, exist_ok=True)

    log_file = os.path.join(carpeta_salida, "a6_matricula.txt")
    diccionario_file = os.path.join(carpeta_salida, "diccionario.txt")

    palabras_globales = Counter()
    archivos_por_palabra = defaultdict(set)

    with open(log_file, "w", encoding="utf-8") as log:
        log.write("Medición de tiempos - Actividad 6\n")
        log.write("------------------------------------------------\n\n")
        tiempo_inicio_total = time.time()

        archivos_html = [f for f in os.listdir(carpeta_html) if f.endswith(".html")]
        if not archivos_html:
            log.write("No se encontraron archivos HTML en la carpeta de entrada.\n")
            return

        # Procesar cada archivo
        for archivo in archivos_html:
            ruta = os.path.join(carpeta_html, archivo)
            inicio = time.time()

            texto_limpio = remover_etiquetas_html(ruta)
            palabras = extraer_palabras(texto_limpio)

            # Contar palabras del archivo y actualizar global
            contador = Counter(palabras)
            for palabra in contador:
                palabras_globales[palabra] += contador[palabra]
                archivos_por_palabra[palabra].add(archivo)

            # Guardar tokens individuales por archivo
            salida_archivo = os.path.join(carpeta_salida, archivo.replace(".html", ".txt"))
            with open(salida_archivo, "w", encoding="utf-8") as f_out:
                for palabra in palabras:
                    f_out.write(palabra + "\n")

            fin = time.time()
            log.write(f"{archivo}: {fin - inicio:.6f} segundos\n")

        # Crear diccionario con tres columnas: palabra, repeticiones, # archivos
        inicio = time.time()
        with open(diccionario_file, "w", encoding="utf-8") as f:
            f.write("Token;Repeticiones;# de archivos\n")
            for palabra, frecuencia in sorted(palabras_globales.items()):
                num_archivos = len(archivos_por_palabra[palabra])
                f.write(f"{palabra};{frecuencia};{num_archivos}\n")
        fin = time.time()
        log.write(f"\nCreación del diccionario: {fin - inicio:.6f} segundos\n")

        tiempo_total = time.time() - tiempo_inicio_total
        log.write("\n------------------------------------------------\n")
        log.write(f"Tiempo total: {tiempo_total:.6f} segundos\n")

if __name__ == "__main__":
    main()
