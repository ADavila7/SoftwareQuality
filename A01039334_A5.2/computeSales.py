"""
computeSales.py - Script que calcula el costo total de todas las ventas incluidas 
en un archivo de tipo JSON, tomando como base los precios de los productos vendidos
en otro archivo de tipo JSON.

Este script lee dos archivos tipo JSON. Del primer archivo se toman los precios de 
cada uno de los elementos en venta, asi como las ventas realizadas y cantidades
vendidas en el segundo archivo. Si el archivo no es compatible, se desplegará un 
mensaje en la consola.

Al finalizar, se imprimen los resultados en la consola y se crea un archivo llamado 
"SalesResults.txt".
"""

#!/usr/bin/env python
# coding: utf-8
# pylint: disable=invalid-name

# In[1]:


import sys
import time
import json

# In[2]:


def open_file(file_path):
    """
    Apertura y lectura de los datos del archivo json. Si el archivo no se encuentra o no
    está en un formato válido, se genera un error.
    """
    try:
        with open(file_path, 'r', encoding= 'utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {file_path} not found. ")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid format. ")
        return None

# In[3]:


def sum_cost(products_list, sales_list):
    """
    Análisis de las ventas en "sales_list" para encontrar el precio de los
    productos en "products_list". Después de eso, se multiplica el precio
    por la cantidad de la venta. Finalmente, suma todos los valores de cada
    venta para obtener el costo total del archivo.
    """
    tot=0
    for sale in sales_list:
        name = sale.get("Product")
        quantity = sale.get("Quantity")
        print(f"Processing sale: {name}, Quantity: {quantity}")
        product = next((product for product in products_list if product["title"] == name), None)
        if product:
            tot += product["price"] * quantity
        else:
            print(f"Product '{name}' not found in products_list")
    return tot

# In[4]:

def main():
    """
    Operación principal cuando se ejecuta el script. Se realiza la suma del costo total
    de las ventas in "sales file". Después de eso, se imprimen los resultados en la consola
    y se escriben en un archivo llamado "SalesResults.txt".
    """
    start_time = time.time()
    #Input of JSON files
    if len(sys.argv) != 3:
        print("Usage: python computeSales.py"
              "priceCatalogue.json salesRecord.json")
        sys.exit(1)
    catalogue_path = sys.argv[1]
    sales_path = sys.argv[2]
    #Read JSON files
    price_catalogue = open_file(catalogue_path)
    sales_record = open_file(sales_path)
    if price_catalogue is None or sales_record is None:
        return
    #Calculate total cost
    tot_cost = sum_cost(price_catalogue, sales_record)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total Cost: ${tot_cost:.2f}")
    print(f"Time Elapsed: {elapsed_time} seconds\n")
    with open("SalesResults.txt", 'w', encoding='utf-8') as result_file:
        sys.stdout = result_file
        result_file.write(f"Total Cost: ${tot_cost:.2f}\n")
        result_file.write(f"Time Elapsed: {elapsed_time} seconds\n")
        sys.stdout = sys.__stdout__

if __name__ == "__main__":
    main()

# In[5]:
