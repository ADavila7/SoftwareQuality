"""
Unit tests for the Hotel class.

This module contains tests that verify the functionality of the Hotel class,
ensuring that all methods behave as expected under various conditions.
"""

import unittest
import os
from hotel import Hotel, Room
from reservation.Reservation import reserve


class TestHotel(unittest.TestCase):
    """Test cases for the Hotel class.

    This class implements unit tests for the Hotel class, covering initial setup,
    room management, and information display functionalities.
    """
    def setUp(self):
        """Setup method to create a hotel and a room instance before each test."""
        self.hotel = Hotel("Test Hotel", "Test Location")
        test_room = Room(room_number=152, room_available=True)
        self.hotel.rooms.append(test_room)
        # Access the room through the hotel
        self.room = self.hotel.rooms[0]

    def test_room_initialization(self):
        """Test the initialization of a room."""
        self.assertEqual(self.room.room_num, 152)
        self.assertTrue(self.room.room_av)

    def test_make_reservation(self):
        """Test making a reservation."""
        self.room.res_room()
        self.assertFalse(self.room.room_av)

    def test_cancel_reservation(self):
        """Test canceling a reservation."""
        self.room.res_room()  # First, make a reservation.
        self.room.cancel_room()
        self.assertTrue(self.room.room_av)

    def test_create_hotel(self):
        """Test creating a hotel correctly initializes its attributes."""
        name = "New Hotel"
        location = "New Location"
        hotel = Hotel.create_hotel(self, name, location)
        self.assertEqual(hotel.name, name, "Hotel name should match the provided name.")
        self.assertEqual(hotel.location, location, "Hotel location should match the provided location.")
        # Cleanup created hotel data file to avoid side effects
        os.remove(hotel.hotel_file)

    def test_delete_hotel(self):
        """Test deleting a hotel removes its data file."""
        hotel = Hotel.create_hotel(self, "Temporary Hotel", "Temporary Location")
        # Ensure the file exists before deletion
        self.assertTrue(os.path.exists(hotel.hotel_file), "Hotel data file should exist before deletion.")
        Hotel.delete_hotel(hotel)
        # Verify the file no longer exists
        self.assertFalse(os.path.exists(hotel.hotel_file), "Hotel data file should be deleted.")

    def test_display_hotel_information(self):
        """Test displaying hotel information"""
        expected_output = "Hotel Name: Test Hotel, Location: Test Location"
        self.assertEqual(self.hotel.display_hotel_information(), expected_output)

    def test_modify_hotel_information(self):
        """Test modifying hotel information updates the hotel attributes."""
        new_name = "Updated Test Hotel"
        new_location = "Updated Test Location"
        self.hotel.modify_hotel_information(new_name=new_name, new_location=new_location)

        # Verify that the hotel's information has been updated
        self.assertEqual(self.hotel.name, new_name, "Hotel name should be updated.")
        self.assertEqual(self.hotel.location, new_location, "Hotel location should be updated.")

    def test_reserve_room(self):
        """Test reserving a room changes its availability."""

        room_number = 152  # Define the room number as a variable

        # Attempt to reserve a room
        result = self.hotel.reserve_room("reservation_id", "customer_id", "Gold", room_number, "2023-01-01", "2023-01-05")

        # Print debug information
        print("Result:", result)
        print("Hotel rooms:", self.hotel.rooms)

        # Assert: Check the room is now reserved (not available)
        reserved_room = next((r for r in self.hotel.rooms if r.room_num == room_number), None)
        self.assertTrue(result, "Room reservation should succeed")
        self.assertIsNotNone(reserved_room, "Reserved room should exist in hotel")
        self.assertFalse(reserved_room.room_av, "Room should be marked as not available after reservation")

    def test_cancel_reservation(self):
        """Test canceling a reservation marks the room as available again."""
        # Setup: Create a hotel, add a room, and make a reservation
        hotel = Hotel("Hotel for Reservation", "Reservation Location")
        room_number = 101
        hotel.rooms.append(Room(room_number, True))
        reservation_id = "res101"
        hotel.reserve_room(reservation_id, "cust101", "Gold", room_number, "2023-01-01", "2023-01-05")

        # Act: Cancel the reservation
        hotel.cancel_reservation(reservation_id)

        # Assert: The room is available again
        room = next((room for room in hotel.rooms if room.room_num == room_number), None)
        self.assertIsNotNone(room, "The room should exist.")
        self.assertTrue(room.room_av, "The room should be available after canceling the reservation.")


if __name__ == '__main__':
    unittest.main()