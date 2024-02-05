"""
computeStatistics.py - Script que calcula las estadísticas descriptivas de los datos en un archivo.

Este script lee un archivo que contiene datos numéricos, con los cuales calcula las estadísticas
descriptivas de estos datos (media, mediana, moda, varianza y desviación estándar). 
Al finalizar, se imprimen los resultados en la consola y se crea un archivo llamado 
StatisticsResults.txt.
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
    Apertura y lectura de los datos numéricos del archivo. Si el valor no es numérico, se despliega
    un error y se lo salta.
    """
    with open(path, 'r', encoding='utf-8') as file:
        data = []
        for line in file.readlines():
            stripped_data = line.strip()
            if stripped_data:
                try:
                    int_number = int(stripped_data)
                    data.append(int_number)
                except ValueError:
                    print(f"Warning: {stripped_data} is not a number and "
                          "will not be taken into account for the conversion.")
        return data


# In[3]:


def calculate_mode(data):
    """
    Calculo de la moda de los datos en el archivo.
    """
    max_count = (0,0)
    for value in data:
        occurences = data.count(value)
        if occurences > max_count[0]:
            max_count = (occurences, value)
    return max_count[1]

# In[4]:

def calculate_mean(data,amount):
    """
    Calculo del promedio de los datos en el archivo.
    """
    total = 0
    if amount == 0:
        return None
    for num in data:
        total=total + num
    return total/amount


# In[5]:

def calculate_median(data,amount):
    """
    Calculo de la mediana de los datos en el archivo.
    """
    data.sort()
    if amount %2 != 0:
        mid_idx = int((amount-1)/2)
        median = data[mid_idx]
        return median
    if amount %2 == 0:
        mid_idx_1 = int(amount/2)
        mid_idx_2 = int(amount/2)-1
        med_mean = (data[mid_idx_1]+data[mid_idx_2])/2
        return med_mean
    return None


# In[6]:

def calculate_variance(data, mean, amount):
    """
    Calculo de la varianza de los datos en el archivo.
    """
    total=0
    for num in data:
        accum=(num-mean)**2
        total=total + accum
    return total/amount


# In[7]:

def calculate_sd(var):
    """
    Calculo de la desviación estándar de los datos en el archivo.
    """
    return var**0.5


# In[8]:

def main():
    """
    Operación principal cuando se ejecuta el script. Se realiza el conteo de los datos
    numéricos de un archivo. Después, se calculan las estadísticas descriptivas de estos
    datos y se imprimen los resultados en la consola. Por último, estos resultados se 
    escriben en un archivo llamado "StatisticsResults.txt".
    """
    start_time = time.time()
    if len(sys.argv) != 2:
        print("Usage: python computeStatistics.py input.txt")
        sys.exit(1)
    file_path = sys.argv[1]
    data = open_file(file_path)
    amount=len(data)
    mean=calculate_mean(data, amount)
    mode=calculate_mode(data)
    median=calculate_median(data, amount)
    variance=calculate_variance(data, mean, amount)
    st_dev=calculate_sd(variance)
    print("Results:")
    print(f"Count: {amount}, Mean: {mean}, Median: {median}, Mode: {mode}, "
    f"Variance: {variance}, Standard Deviation: {st_dev}")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time Elapsed: {elapsed_time} seconds\n")
    with open("StatisticsResults.txt", 'w', encoding='utf-8') as result_file:
        # Redirect stdout to the file
        sys.stdout = result_file
        print("Results:")
        print(f"Count: {amount}, Mean: {mean}, Median: {median}, Mode: {mode}, "
        f"Variance: {variance}, Standard Deviation: {st_dev}")
        sys.stdout = sys.__stdout__

if __name__ == "__main__":
    main()

# In[9]:
