from typing import List, Tuple
from inputValidation import Validation
from tabulate import tabulate  # For clean table formatting


class Room:
    """Represents a hotel room with number, type, price, and bookings."""

    def __init__(self, conn):
        self.cursor = conn.cursor()

    def rooms_menu(self, Hotel):
        """Displays the room management menu and handles user selection."""
        print("\n\033[0;0mRooms Menu Options:\n"
              "\033[95m1.\033[0;0m Available Rooms\n"
              "\033[95m2.\033[0;0m Booked Rooms\n"
              "\033[95m3.\033[0;0m Maintenance Rooms\n"
              "\033[95m4.\033[0;0m Search Room\n"
              "\033[95m5.\033[0;0m Main Menu\n")

        selected_option = input("Select a number: ")
        status, value = Validation.validate_text_input(input_text=selected_option, min_value=1, max_value=5)

        if not status:
            print(value)
            return self.rooms_menu(Hotel)

        print(chr(27) + "[2J")  # Clear screen

        menu_actions = {
            1: self.print_available_rooms,
            2: self.print_booked_rooms,
            3: self.print_maintenance_rooms,
            4: self.search_room,
            5: Hotel.main_menu
        }

        action = menu_actions.get(value)
        if action:
            if value in {1, 2, 3}:
                action()
                self.rooms_menu(Hotel)
            elif value == 4:
                self.search_room()
                self.rooms_menu(Hotel)
            else:
                action()

    def print_available_rooms(self):
        """Prints all available rooms."""
        print("Available Rooms:")
        rooms = self.query_rooms_by_status('Available')
        self.display_rooms(rooms)

    def print_booked_rooms(self):
        """Prints all occupied/booked rooms."""
        print("Booked Rooms:")
        rooms = self.query_rooms_by_status('Occupied')
        self.display_rooms(rooms)

    def print_maintenance_rooms(self):
        """Prints all rooms under maintenance."""
        print("Maintenance Rooms:")
        rooms = self.query_rooms_by_status('Maintenance')
        self.display_rooms(rooms)

    def search_room(self):
        """Prompts for a room ID and displays its details."""
        try:
            room_id = int(input("Please enter a room number: "))
            self.print_room(room_id)
        except ValueError:
            print("Invalid room number entered.")

    def print_room(self, room_id):
        """Prints detailed info about a specific room."""
        print(f"Room {room_id}:")
        self.cursor.execute('SELECT * FROM ROOMS WHERE ID = ?', (room_id,))
        room = self.cursor.fetchone()
        if room:
            headers = ['Room ID', 'Type', 'Amenities', 'Price', 'Status']
            print(tabulate([room], headers=headers, tablefmt='grid'))
        else:
            print("Room not found.")

    def display_rooms(self, rooms: List[Tuple[int, str, str, float, str]]):
        """Helper to print a list of rooms in tabular format."""
        if rooms:
            headers = ['Room ID', 'Type', 'Amenities', 'Price', 'Status']
            print(tabulate(rooms, headers=headers, tablefmt='grid'))
        else:
            print("No rooms to display.")

    def query_rooms_by_status(self, status: str) -> List[Tuple[int, str, str, float, str]]:
        """Returns all rooms with a specific status."""
        self.cursor.execute('SELECT * FROM ROOMS WHERE STATUS = ?', (status,))
        return self.cursor.fetchall()
