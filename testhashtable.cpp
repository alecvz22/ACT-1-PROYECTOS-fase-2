#include <iostream>
#include "hashtable.h"

using namespace std;

int main() {
    const unsigned long HT_SIZE = 500;
    HashTable Ht(HT_SIZE);

    // Imprimir vacío
    Ht.Print("dict.txt");

    // Insertar valores
    Ht.Insert("Susan", 9);
    Ht.Insert("John", 6);
    Ht.Insert("David", 42);

    // Imprimir tabla con datos
    Ht.Print("dict.txt");

    // Obtener dato
    cout << "David's magic number is: " << Ht.GetData("David") << endl;

    return 0;
}
