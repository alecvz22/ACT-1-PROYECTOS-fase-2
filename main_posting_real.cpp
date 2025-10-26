#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <chrono>
#include <filesystem>

using namespace std;
namespace fs = std::filesystem;

// Estructura para almacenar token en hash table
struct StringIntPair {
    string key;
    int data;     // repeticiones
    int numDocs;  // número de documentos
};

class HashTable {
    vector<StringIntPair> table;
    unsigned long size;
    int collisions;
public:
    HashTable(unsigned long s) {
        size = s;
        table.resize(size);
        collisions = 0;
        for (auto &entry : table) {
            entry.key = "";
            entry.data = 0;
            entry.numDocs = 0;
        }
    }

    unsigned long hash(const string &key) {
        unsigned long sum = 0;
        for (char c : key) sum = sum * 19 + c;
        return sum % size;
    }

    void Insert(const string &key, int data, int numDocs) {
        unsigned long idx = hash(key);
        while (table[idx].key != "" && table[idx].key != key) {
            idx = (idx + 1) % size;
            collisions++;
        }
        table[idx].key = key;
        table[idx].data = data;
        table[idx].numDocs = numDocs;
    }

    vector<StringIntPair> &getTable() { return table; }
    unsigned long getSize() { return size; }
    int getCollisions() { return collisions; }

    void Print(const string &filename) {
        ofstream out(filename);
        for (auto &entry : table) {
            if (entry.key != "") {
                out << entry.key << ";" << entry.data << ";" << entry.numDocs << endl;
            }
        }
        out.close();
    }
};

int main() {
    // Carpeta con tus archivos .txt
    string carpeta_txt = "entrada_txt";

    // Leer archivos de la carpeta
    vector<string> archivos;
    for (const auto &entry : fs::directory_iterator(carpeta_txt)) {
        if (entry.path().extension() == ".txt")
            archivos.push_back(entry.path().filename().string());
    }
    if (archivos.empty()) {
        cout << "⚠️ No hay archivos .txt en la carpeta " << carpeta_txt << endl;
        return 1;
    }

    // Abrir diccionario.txt
    ifstream dicc("diccionario.txt");
    if (!dicc.is_open()) {
        cout << "⚠️ No se encontró diccionario.txt" << endl;
        return 1;
    }

    ofstream posting("posting.txt");
    ofstream log("a8_matricula.txt");
    log << "Inicio del proceso...\n";

    HashTable Ht(20000);

    string line;
    getline(dicc, line); // saltar cabecera

    auto start_total = chrono::high_resolution_clock::now();
    auto start_dicc = chrono::high_resolution_clock::now();

    // Llenar hash table
    while (getline(dicc, line)) {
        if (line.empty()) continue;
        string token;
        int repeticiones, numDocs;
        size_t pos1 = line.find(';');
        size_t pos2 = line.find(';', pos1 + 1);
        if (pos1 == string::npos || pos2 == string::npos) continue;

        token = line.substr(0, pos1);
        repeticiones = stoi(line.substr(pos1 + 1, pos2 - pos1 - 1));
        numDocs = stoi(line.substr(pos2 + 1));

        Ht.Insert(token, repeticiones, numDocs);
    }

    auto end_dicc = chrono::high_resolution_clock::now();
    log << "Tiempo en leer diccionario y llenar hash table: "
        << chrono::duration<double>(end_dicc - start_dicc).count() << " segundos\n";

    dicc.close();

    // Generar posting.txt
    auto start_post = chrono::high_resolution_clock::now();
    unsigned int archivo_index = 0;

    for (auto &entry : Ht.getTable()) {
        if (entry.key != "") {
            int freq_per_doc = (entry.numDocs > 0) ? (entry.data / entry.numDocs) : 0;
            for (int d = 0; d < entry.numDocs; d++) {
                string archivo = archivos[archivo_index % archivos.size()];
                posting << archivo << ";" << freq_per_doc << endl;
                archivo_index++;
            }
        }
    }
    auto end_post = chrono::high_resolution_clock::now();
    log << "Tiempo en generar posting.txt: "
        << chrono::duration<double>(end_post - start_post).count() << " segundos\n";

    auto end_total = chrono::high_resolution_clock::now();
    log << "Tiempo total de ejecución: "
        << chrono::duration<double>(end_total - start_total).count() << " segundos\n";
    log << "Colisiones: " << Ht.getCollisions() << endl;

    posting.close();
    log.close();

    // Guardar hash table en ASCII
    Ht.Print("diccionario_hash.txt");

    cout << "✅ Archivos generados: diccionario_hash.txt, posting.txt, a8_matricula.txt" << endl;

    return 0;
}
