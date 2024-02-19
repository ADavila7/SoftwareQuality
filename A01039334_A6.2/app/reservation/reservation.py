"""
Module for managing reservations in the hotel reservation system.

Author: Adrián Dávila
Last Edited: 18/February/2024
"""

# pylint: disable=invalid-name

# In[1]:


import json
import os


# In[2]:


class Reservation:
    """
    Representation of a reservation into the hotel reservation system.
    
    Attributes:
        customer_id (int): The customer's who made the reservation ID.
        rez_id (int): The reservation's unique ID.
        customer_sts (str): The customer's current status in the hotel system.
        hotel_id (str): The name of the hotel where the reservation is made.
        room_num (int): The room number that is being reserved.
        start_date (str): The starting date of the reservation.
        end_date (str): The ending date of the reservation.
    """

    def __init__(self, **kwargs):
        """Initialization of a reservation in the hotel."""
        self.customer_id = kwargs.get('customer_id')
        self.rez_id = kwargs.get('rez_id')
        self.customer_sts = kwargs.get('customer_status')
        self.hotel_id = kwargs.get('hotel_id')
        self.room_num = kwargs.get('room_number')
        self.start_date = kwargs.get('start_date')
        self.end_date = kwargs.get('end_date')

    def save_data(self):
        """Saving of reservation details to a JSON file."""
        data = vars(self)
        rez_file = f"reservation_{self.rez_id}.json"
        with open(rez_file, 'w', encoding='utf-8') as f:
            json.dump(data, f)

    def cancel_reservation(self, rez_id):
        """Canceling of a reservation in a hotel by removing
        its information from a JSON file."""
        rez_file = f"reservation_{rez_id}.json"
        if os.path.exists(rez_file):
            os.remove(rez_file)
            print("Reservation canceled successfully.")
        else:
            print(f"Reservation with ID {rez_id} not found.")

    def create_reservation(self, cls, **kwargs):
        """Creation of a reservation in a hotel."""
        res = cls(**kwargs)
        res.save_data()
        print("Reservation created successfully.")
        return res


def reserve(**kwargs):
    """Function to be called from hotel.py to generate a room
    reservation with these file methods."""
    return Reservation(**kwargs)
