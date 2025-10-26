import os
import sys
import time
import math
from collections import defaultdict, Counter

def cargar_diccionario(ruta_dicc):
    """Lee diccionario.txt y devuelve un dict token -> num_archivos"""
    dicc_tokens = {}
    with open(ruta_dicc, "r", encoding="utf-8") as f:
        next(f)  # saltar cabecera
        for linea in f:
            partes = linea.strip().split(";")
            if len(partes) == 3:
                token, repeticiones, num_docs = partes
                dicc_tokens[token] = int(num_docs)
    return dicc_tokens

def leer_archivos_txt(carpeta_txt):
    """Lee todos los archivos .txt y devuelve dict archivo -> lista de palabras"""
    archivos = {}
    for nombre in os.listdir(carpeta_txt):
        if nombre.endswith(".txt"):
            ruta = os.path.join(carpeta_txt, nombre)
            with open(ruta, "r", encoding="utf-8") as f:
                palabras = f.read().lower().split()
                archivos[nombre] = palabras
    return archivos

def calcular_tfidf(diccionario, archivos, log_file, posting_file):
    log = open(log_file, "w", encoding="utf-8")
    log.write("Actividad 10: TF-IDF Weight Tokens\n")
    log.write("------------------------------------------------\n\n")
    tiempo_inicio_total = time.time()

    # Contar cuántos documentos contienen cada token
    doc_count = defaultdict(int)
    for archivo, palabras in archivos.items():
        for token in set(palabras):
            if token in diccionario:
                doc_count[token] += 1

    # Crear posting con TF-IDF
    with open(posting_file, "w", encoding="utf-8") as posting:
        posting.write("Archivo;Token;TF-IDF\n")
        for archivo, palabras in archivos.items():
            inicio_archivo = time.time()
            total_palabras = len(palabras)
            counter = Counter(palabras)
            for token, tf in counter.items():
                if token in diccionario:
                    # TF-IDF clásico
                    idf = math.log(len(archivos) / doc_count[token]) if doc_count[token] > 0 else 0
                    tfidf = (tf / total_palabras) * idf
                    posting.write(f"{archivo};{token};{tfidf:.6f}\n")
            fin_archivo = time.time()
            log.write(f"{archivo}: {fin_archivo - inicio_archivo:.6f} segundos\n")

    tiempo_total = time.time() - tiempo_inicio_total
    log.write(f"\nTiempo total de ejecución: {tiempo_total:.6f} segundos\n")
    log.close()

    print("✅ TF-IDF calculado correctamente")
    print(f"- {posting_file}")
    print(f"- {log_file}")

def main():
    carpeta_txt = "txt"          # tus archivos tokenizados
    carpeta_salida = "salida"    # diccionario.txt

    os.makedirs(carpeta_txt, exist_ok=True)
    os.makedirs(carpeta_salida, exist_ok=True)

    ruta_dicc = os.path.join(carpeta_salida, "diccionario.txt")
    posting_file = os.path.join(carpeta_salida, "posting_tfidf.txt")
    log_file = os.path.join(carpeta_salida, "a10_matricula.txt")

    if not os.path.exists(ruta_dicc):
        print(f"⚠️ No se encontró '{ruta_dicc}'")
        return

    archivos = leer_archivos_txt(carpeta_txt)
    if not archivos:
        print(f"⚠️ No se encontraron archivos .txt en la carpeta '{carpeta_txt}'")
        return

    diccionario = cargar_diccionario(ruta_dicc)
    calcular_tfidf(diccionario, archivos, log_file, posting_file)

if __name__ == "__main__":
    main()
