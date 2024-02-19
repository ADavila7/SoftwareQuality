"""
Module for managing hotel information in the hotel reservation system.

Author: Adrián Dávila
Last Edited: 18/February/2024
"""

# pylint: disable=invalid-name

# In[1]:


import json
import os
from reservation.Reservation import reserve


# In[2]:


class Room:
    """ Representation of a room from the hotel reservation system. """
    def __init__(self, room_number, room_available=True):
        """ Initializing of Room instance. """
        self.room_num = room_number
        self.room_av = room_available

    def res_room(self):
        """Marks the selected room as reserved (not available)."""
        self.room_av = False

    def cancel_room(self):
        """Marks the selected room as available (cancels reservation)."""
        self.room_av = True

    @classmethod
    def from_dict(cls, room_data):
        """Creates a Room instance from a dictionary.

        Parameters:
            data (dict): A dictionary containing the room information.

        Returns:
            Room: An instance of the room class.
        """
        return cls(
            room_number=room_data['room_number'],
            room_available=room_data.get('room_available', True)
        )

    def to_dict(self):
        """
        Converts the Room instance into a dictionary representation.

        This method allows the Room object's current state to be represented
        as a dictionary, making it easier to serialize, especially for saving
        the room data in formats like JSON.

        Returns:
            dict: A dictionary containing the room's properties.
        """
        return {
            'room_number': self.room_num,
            'room_available': self.room_av
        }


class Hotel:
    """
    Representation of a hotel from the hotel reservation system.
    
    Attributes:
        name (str): The hotel's name.
        location (str): The hotel's site location.
        room_number (int): The room number.
        is_available (bool): Availability status of the room.
    """
    def __init__(self, name, location):
        """Initializes a Hotel object with a name and location.
        Defines an empty room list, initially defines all rooms as
        available and reads the room number to reserve."""
        self.name = name
        self.location = location
        self.rooms = []
        self.hotel_file = f"{name}_data.json"

    def save_data(self):
        """Saving of hotel information on a JSON file."""
        data = {
            'name': self.name,
            'location': self.location,
            'rooms': [room.to_dict() for room in self.rooms]
        }
        with open(self.hotel_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2)

    def load_from_file(self):
        """Loading of hotel information from a JSON file."""
        with open(self.hotel_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        self.name = data['name']
        self.location = data['location']
        self.rooms = [Room.from_dict(room_data) for room_data in data['rooms']]  # pylint: disable=no-member

    def create_hotel(self, name, location):
        """Creation of a new hotel and saving of this information into
        a JSON file."""
        hotel = Hotel(name, location)
        hotel.save_data()
        print("Hotel has been created succesfully.")
        return hotel

    def delete_hotel(self):
        """Deletion of a hotel's information file."""
        os.remove(self.hotel_file)
        print("Hotel has been deleted succesfully.")

    def display_hotel_information(self):
        """Returns hotel information as a string."""
        print (f"""Hotel Name: {self.name}, Location: {self.location}""")

    def modify_hotel_information(self, new_name=None, new_location=None):
        """Modification of customer's data in a file."""
        if new_name:
            self.name = new_name
        if new_location:
            self.location = new_location
        self.save_data()
        print("Hotel information has been updated.")

    def reserve_room(self, rez_id, customer_id, customer_sts,   # pylint: disable=too-many-arguments
                     room_num, start_date, end_date):
        """Reservation of a room if available."""
        room = next((room for room in self.rooms if room.room_num == room_num
        and room.room_available), None)
        if room:
            room.res_room()
            reservation = reserve(
                rez_id=rez_id,
                customer_id=customer_id,
                hotel_id=self.name,
                customer_sts=customer_sts,
                room_num=room_num,
                start_date=start_date,
                end_date=end_date
            )
            reservation.save_data()
            self.save_data()
            return True
        return False

    def cancel_reservation(self, rez_id):
        """Canceling of a room reservation."""
        try:
            with open(f"reservation_{rez_id}.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
            room_num = data['room_number']
            room = next((room for room in self.rooms if room.room_num == room_num), None)
            if room:
                room.cancel_room()
                os.remove(f"reservation_{rez_id}.json")
                self.save_data()
                return True
        except FileNotFoundError:
            pass
        return False
