import os
import re
import time
import subprocess
import matplotlib.pyplot as plt

# -------------------------------
# Comando simulado: tokenize
# -------------------------------
def comando_tokenize(input_dir, output_dir):
    """Simula el comando 'tokenize input-dir output-dir'"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(input_dir, filename), "r", encoding="utf-8") as f:
                texto = f.read().lower()
            tokens = re.findall(r"\b\w+\b", texto)
            with open(os.path.join(output_dir, f"tok_{filename}"), "w", encoding="utf-8") as f:
                f.write(" ".join(tokens))

# -------------------------------
# Comando simulado: index
# -------------------------------
def comando_index(input_dir, output_dir):
    """Simula el comando 'index input-dir output-dir'"""
    indice = {}

    for filename in os.listdir(input_dir):
        if filename.startswith("tok_") and filename.endswith(".txt"):
            with open(os.path.join(input_dir, filename), "r", encoding="utf-8") as f:
                tokens = f.read().split()
            for token in tokens:
                if token not in indice:
                    indice[token] = set()
                indice[token].add(filename)

    # Guardar índice invertido
    with open(os.path.join(output_dir, "indice.txt"), "w", encoding="utf-8") as f:
        for token, archivos in sorted(indice.items()):
            f.write(f"{token}: {', '.join(sorted(archivos))}\n")

# -------------------------------
# Ejecutar comandos como llamadas DOS/Unix simuladas
# -------------------------------
def ejecutar_comando(nombre, input_dir, output_dir):
    """Ejecuta un comando simulado (tokenize o index)"""
    if nombre == "tokenize":
        comando_tokenize(input_dir, output_dir)
    elif nombre == "index":
        comando_index(input_dir, output_dir)
    else:
        print(f"⚠️ Comando desconocido: {nombre}")

# -------------------------------
# Mide tiempo de tokenización + indexación
# -------------------------------
def medir_tiempo(input_dir, output_dir, n):
    """Ejecuta las llamadas 'tokenize' e 'index' y mide su tiempo"""
    # Crear carpeta temporal con n archivos
    temp_dir = "temp_docs"
    os.makedirs(temp_dir, exist_ok=True)

    for archivo in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, archivo))

    for i, nombre in enumerate(sorted(os.listdir(input_dir))):
        if nombre.endswith(".txt") and i < n:
            with open(os.path.join(input_dir, nombre), "r", encoding="utf-8") as src:
                with open(os.path.join(temp_dir, nombre), "w", encoding="utf-8") as dst:
                    dst.write(src.read())

    # Tokenizar + Indexar
    inicio = time.time()
    ejecutar_comando("tokenize", temp_dir, output_dir)
    ejecutar_comando("index", output_dir, output_dir)
    fin = time.time()

    return fin - inicio

# -------------------------------
# Programa principal
# -------------------------------
def main():
    input_dir = "entrada"   # Carpeta con documentos originales
    output_dir = "salida"   # Carpeta de salida

    if not os.path.exists(input_dir):
        print(f"⚠️ No se encontró la carpeta '{input_dir}'")
        return

    documentos = [10, 20, 30, 40, 50]
    tiempos = []

    for n in documentos:
        print(f"\n🔹 Procesando {n} documentos...")
        t = medir_tiempo(input_dir, output_dir, n)
        tiempos.append(t)
        print(f"⏱️ Tiempo total ({n} docs): {t:.4f} segundos")

    # Graficar resultados
    plt.plot(documentos, tiempos, marker="o")
    plt.title("Tiempo de tokenización + indexación")
    plt.xlabel("Número de documentos")
    plt.ylabel("Tiempo (segundos)")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
