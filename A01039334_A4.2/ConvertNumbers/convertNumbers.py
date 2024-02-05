"""
convertNumbers.py - Script que convierte números decimales a binario y hexadecimal.

Este script lee un archivo que contiene datos numéricos, descarta los valores que no son números
y convierte los números a su notación binaria y hexadecimal. Al finalizar, se imprimen los
resultados en la consola y se crea un archivo llamado ConvertionResults.txt.
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


def find_max_bit(data):
    """
    Búsqueda del mayor número de bits que se necesitan para las conversiones.
    """
    max_abs = 0
    num_bits = 1
    for number in data:
        abs_val = abs(number)
        if abs_val > max_abs:
            max_abs = abs_val
    max_bit = 1
    while max_bit < max_abs + 1:
        max_bit *= 2
        num_bits = num_bits +1
    max_rem = num_bits % 4
    if max_rem == 0:
        return num_bits
    max_bits = num_bits + (4 - max_rem)
    return max_bits


# In[4]:

def decimal_binary(number, num_bits):
    """
    Conversión de un número decimal a un número binario. Se usan
    los complementos de 2's para los números negativos.
    """
    bin_number = ""
    if number < 0:
        sign = "1"
    else:
        sign = "0"
    number = abs(number)
    while number > 0:
        bin_number = str(number % 2) + bin_number
        number //=2
    while len(bin_number) < num_bits:
        bin_number = '0' + bin_number
    if sign == "1":
        bin_number = "".join("1" if bit == "0" else "0" for bit in bin_number)
        carry = 1
        for i in range(len(bin_number) - 1, -1, -1):
            if carry == 1:
                if bin_number[i] == "0":
                    bin_number = bin_number[:i] + "1" + bin_number[i + 1:]
                    carry = 0
                else:
                    bin_number = bin_number[:i] + "0" + bin_number[i + 1:]
        if carry == 1:
            bin_number = "1" + bin_number
    return bin_number, sign

# In[5]:

def decimal_hexadecimal(bin_number, sign):
    """
    Conversión de un número binario a hexadecimal. Cuando se tiene un número
    negativo, se usan 10 dígitos.
    """
    bin_to_hex_dict = {
        '0000': '0', '0001': '1', '0010': '2', '0011': '3',
        '0100': '4', '0101': '5', '0110': '6', '0111': '7',
        '1000': '8', '1001': '9', '1010': 'A', '1011': 'B',
        '1100': 'C', '1101': 'D', '1110': 'E', '1111': 'F'
    }
    hex_number = ''
    if bin_number == "0":
        return "0"
    for i in range(0, len(bin_number), 4):
        bin_set = bin_number[i:i+4]
        hex_dig = bin_to_hex_dict[bin_set]
        hex_number += hex_dig
    if sign == "1":
        while len(hex_number) < 10:
            hex_number = 'F' + hex_number
    return hex_number

# In[6]:

def main():
    """
    Operación principal cuando se ejecuta el script. Se realiza la conversión
    de un número decimal a binario. Después, se toma este resultado y se convierte
    a hexadecimal y se imprimen los tres resultados en la consola. Por último,
    esttos resultados se escriben en un archivo llamado "ConvertionResults".
    """
    start_time = time.time()
    if len(sys.argv) != 2:
        print("Usage: python convertNumbers.py input.txt")
        sys.exit(1)
    path = sys.argv[1]
    data = open_file(path)
    num_bits = find_max_bit(data)
    conversion_results = []
    for number in data:
        decimal = decimal_binary(number, num_bits)
        hexadecimal = decimal_hexadecimal(decimal[0], decimal[1])
        conversion_results.extend([(number, decimal[0], hexadecimal)])
    print("Results:")
    for index, (decimal, binary, hexadecimal) in enumerate(conversion_results, start=1):
        print(f"{index} Decimal: {decimal}, Binary: {binary}, Hexadecimal: {hexadecimal}")
    end_time = time.time()
    elapsed_time = end_time - start_time 
    print(f"Time Elapsed: {elapsed_time} seconds\n")
    with open("ConvertionResults.txt", 'w', encoding='utf-8') as result_file:
        # Redirect stdout to the file
        sys.stdout = result_file
        print("Results:")
        for index, (decimal, binary, hexadecimal) in enumerate(conversion_results, start=1):
            print(f"{index} Decimal: {decimal}, Binary: {binary}, Hexadecimal: {hexadecimal}")
        sys.stdout = sys.__stdout__

if __name__ == "__main__":
    main()

# In[7]:
