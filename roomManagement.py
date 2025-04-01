from typing import List, Tuple
from inputValidation import Validation
from tabulate import tabulate  # For clean table formatting


class Room:
    """Represents a hotel room with number, type, price, and bookings."""

    def __init__(self, conn):
        self.cursor = conn.cursor()

    def rooms_menu(self, Hotel):
        print("\n\033[0;0mRooms Menu Options:\n"
              "\033[95m1.\033[0;0m Available Rooms\n"
              "\033[95m2.\033[0;0m Booked Rooms\n"
              "\033[95m3.\033[0;0m Maintanance Rooms\n"
              "\033[95m4.\033[0;0m Search Room\n"
              "\033[95m5.\033[0;0m Main Menu\n")
        selected_option = input("Select a number: ")
        status, value = Validation.validate_text_input(input_text=selected_option, min_value=1, max_value=5)
        if status == False:
            print(value)
            self.rooms_menu(Hotel)
        else:
            print(chr(27) + "[2J")
            match value:
                case 1:
                    # Rooms
                    self.print_available_rooms()
                    self.rooms_menu(Hotel)
                case 2:
                    # Rooms
                    self.print_booked_rooms()
                    self.rooms_menu(Hotel)
                case 3:
                    # Rooms
                    self.print_maintanance_rooms()
                    self.rooms_menu(Hotel)
                case 4:
                    # Rooms
                    room_id = int(input("Please select a room number: "))
                    self.print_room(room_id)
                    self.rooms_menu(Hotel)

                case 5:
                    Hotel.main_menu()

                case 1:
                    # Rooms
                    print("rooms")


    def print_available_rooms(self):
        print("Available Rooms:")
        rooms = self.query_rooms_by_status('Available')
        headers = ['Room ID', 'Type', 'Amenities', 'Price', 'Status']
        print(tabulate(rooms, headers=headers, tablefmt='grid'))


    def print_booked_rooms(self):
        print("Booked Rooms:")
        rooms = self.query_rooms_by_status('Occupied')
        headers = ['Room ID', 'Type', 'Amenities', 'Price', 'Status']
        print(tabulate(rooms, headers=headers, tablefmt='grid'))

    def print_maintanance_rooms(self):
        print("Maintenance Rooms:")
        rooms = self.query_rooms_by_status('Maintenance')
        headers = ['Room ID', 'Type', 'Amenities', 'Price', 'Status']
        print(tabulate(rooms, headers=headers, tablefmt='grid'))

    def print_room(self, room_id):
        print(f"Rooms {room_id}:")
        self.cursor.execute('SELECT * FROM ROOMS WHERE ID = ?', (room_id,))
        room = self.cursor.fetchone()
        if room:
            headers = ['Room ID', 'Type', 'Amenities', 'Price', 'Status']
            print(tabulate([room], headers=headers, tablefmt='grid'))
        else:
            print("Room not found.")


    def query_rooms_by_status(self, status: str) -> List[Tuple[int, str, str, float, str]]:
        self.cursor.execute('SELECT * FROM ROOMS WHERE STATUS = ?', (status,))
        return self.cursor.fetchall()
