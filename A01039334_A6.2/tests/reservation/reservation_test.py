"""
Unit tests for the Reservation class.

This module contains tests that verify the functionality of the Reservation class,
ensuring that all methods behave as expected under various conditions.
"""

import unittest
import os
from reservation import Reservation, reserve


class TestReservation(unittest.TestCase):
    """Tests for functionality of the Reservation class."""
    def setUp(self):
        """Setup method to create a reservation instance before each test."""
        self.reservation_data = {
            'rez_id': 496,
            'customer_sts': 'Gold',
            'customer_id': 501,
            'hotel_id': 'Palm Beach Resorts',
            'room_num': 101,
            'start_date': '2024-03-01',
            'end_date': '2024-03-09'
        }
        self.reservation = reserve(**self.reservation_data)

    def test_reservation_initialization(self):
        """Test the initialization of a reservation."""
        for key, value in self.reservation_data.items():
            self.assertEqual(getattr(self.reservation, key), value, f"Failed for attribute: {key}")

    def test_save_data(self):
        """Test saving a reservation details to a file."""
        self.reservation.save_data()
        expected_filename = f"reservation_{self.reservation.rez_id}.json"
        self.assertTrue(os.path.exists(expected_filename))
        # Clean up
        os.remove(expected_filename)

    def test_cancel_reservation(self):
        """Test canceling a reservation by removing its file."""
        self.reservation.save_data()
        Reservation.cancel_reservation(self, self.reservation.rez_id)
        expected_filename = f"reservation_{self.reservation.rez_id}.json"
        self.assertFalse(os.path.exists(expected_filename))

    def test_rez_id_not_found(self):
        """Test having a different reservation id to delete."""
        self.reservation.save_data()
        Reservation.cancel_reservation(self, "5")
        expected_filename = f"reservation_{self.reservation.rez_id}.json"
        self.assertTrue(os.path.exists(expected_filename))

    def test_create_reservation(self):
        """Test creating a reservation."""
        self.reservation.save_data()
        new_reservation_id = "5"
        Reservation.create_reservation(**self.reservation_data)
        expected_filename = f"reservation_{self.reservation.rez_id}.json"
        self.assertTrue(os.path.exists(expected_filename))


if __name__ == '__main__':
    unittest.main()
