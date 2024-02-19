"""
Module for managing customer information in the hotel reservation system.

Author: Adrián Dávila
Last Edited: 18/February/2024
"""

# pylint: disable=invalid-name

# In[1]:


import json
import os


# In[2]:


class Customer:
    """
    Representation of a customer in the hotel reservation system.
    
    Attributes:
        name (str): The customer's who made the reservation name.
        email (str): The customer's who made the reservation email.
        customer_id (int): The customer's who made the reservation ID.
    """

    def __init__(self, name, email, customer_id):
        """Initialization of a Customer object with ID, name, and email."""
        self.name = name
        self.email = email
        self.customer_id = customer_id
        self.customer_file = f"customer_{customer_id}.json"

    def save_data(self):
        """Saving of customer information on a JSON file."""
        data = {
            'name': self.name,
            'email': self.email,
            'customer_id': self.customer_id
        }
        with open(self.customer_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2)

    def create_customer(self, name, email, customer_id):
        """Creation of a new customer and saving of the information into a file."""
        customer = Customer(name, email, customer_id)
        customer.save_data()
        return customer

    def display_customer_information(self):
        """Display of a customer's information."""
        print (f"""Name: {self.name}, E-mail: {self.email},
        Customer ID: {self.customer_id}""")

    def delete_customer(self, customer_id):
        """Deletion of a customer's information file."""
        customer_file = f"customer_{customer_id}.json"
        os.remove(customer_file)

    def modify_customer_information(self, name=None, email=None):
        """Modification of customer's data in a file."""
        if name:
            self.name = name
        if email:
            self.email = email
        self.save_data()

    def load_customer(self, customer_id):
        """Loading of a customer's information from a file."""
        customer_file = f"customer_{customer_id}.json"
        with open(customer_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return Customer(data['name'],data['email'],data['customer_id'])
