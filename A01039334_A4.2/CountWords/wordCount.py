"""
wordCount.py - Script que cuenta el número de apariciones de una palabra dentro de un archivo.

Este script lee un archivo que contiene palabras, descartando los valores que no son palabras
(o solamente letras).
Después se imprimen los resultados en la consola y se crea un archivo llamado "WordCountResults.txt" 
"""

#!/usr/bin/env python
# coding: utf-8
# pylint: disable=invalid-name

# In[1]:


import sys
import time

# In[2]:


def open_file(path):
    """
    Apertura y lectura de los datos de un archivo. Si el valor no es una palabra,
    se despliega un error y no lo toma en cuenta.
    """
    with open(path, 'r', encoding='utf-8') as file:
        data = []
        for line in file.readlines():
            stripped_data = line.strip()
            if stripped_data and stripped_data.isalpha():
                data.append(stripped_data)
            else:
                print(f"Warning: {stripped_data} is not a word and "
                      "will not be taken into account")
        return data


# In[3]:

def count_occurrences(words, curr_word):
    """
    Cuenta el número de apariciones de una palabra dentro de un arreglo.
    Después, elimina esas palabras del arreglo para que no se tomen en
    cuenta en la siguiente ejecución.
    """
    count = 0
    i = 0

    while i < len(words):
        if curr_word == words[i]:
            count += 1
            del words[i]
        else:
            i += 1

    return count

# In[4]:

def main():
    """
    Función principal cuando se ejecuta el script. Cuenta la cantidad de apariciones
    individuales de las palabras en el archivo e imprime los resultados en la consola.
    Después se escriben en un archivo llamado "WordCountResults.txt".
    """
    start_time = time.time()
    if len(sys.argv) != 2:
        print("Usage: python convertNumbers.py input.txt")
        sys.exit(1)
    path = sys.argv[1]
    data = open_file(path)
    occurrences = {}
    while data:
        current_word = data[0]
        count = count_occurrences(data, current_word)
        occurrences[current_word] = count
        data = data[1:]
    print("Results:")
    for index, (word, count) in enumerate(occurrences.items(), start=1):
        print(f"{index} Word: {word}, Occurrences: {count}")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time Elapsed: {elapsed_time} seconds\n")
    with open("WordCountResults.txt", 'w', encoding='utf-8') as result_file:
        # Redirect stdout to the file
        sys.stdout = result_file
        print("Results:")
        for index, (word, count) in enumerate(occurrences.items(), start=1):
            print(f"{index} Word: {word}, Occurrences: {count}")
        sys.stdout = sys.__stdout__

if __name__ == "__main__":
    main()

# In[5]:
