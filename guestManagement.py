from inputValidation import Validation
from tabulate import tabulate
from typing import List, Tuple


class Guest:
    def __init__(self, conn):
        self.cursor = conn.cursor()
        self.conn = conn

    def guest_menu(self, Hotel):
        """Displays the guest management menu and handles user input."""
        print("\n\033[0;0mAvailable options:\n"
              "\033[95m1.\033[0;0m New Booking\n"
              "\033[95m2.\033[0;0m List all Guests\n"
              "\033[95m3.\033[0;0m Find Guest\n"
              "\033[95m4.\033[0;0m Update Guest Information\n"
              "\033[95m5.\033[0;0m Main Menu\n")
        selected_option = input("Select a number: ")
        status, value = Validation.validate_text_input(input_text=selected_option, min_value=1, max_value=5)
        if not status:
            print(value)
            return self.guest_menu(Hotel)

        actions = {
            1: self.create_new_booking,
            2: self.display_all_guests,
            3: self.lookup_guest_by_room,
            4: self.update_guest_by_room,
            5: Hotel.main_menu
        }

        action = actions.get(value)
        if action:
            action() if value == 5 else (action(), self.guest_menu(Hotel))

    def display_all_guests(self):
        """Displays all guests and their associated room info in tabular format."""
        self.cursor.execute('''
            SELECT B.ROOM_ID, G.NAME, G.EMAIL, G.PHONE, G.LOYALTY_STATUS
            FROM GUESTS G
            JOIN BOOKINGS B ON G.GUEST_ID = B.GUEST_ID
        ''')
        guests = self.cursor.fetchall()
        headers = ["Room Number", "Name", "Email", "Phone", "Loyalty Status"]
        print(tabulate(guests, headers=headers, tablefmt="grid"))

    def insert_guest(self, name: str, email: str, phone: str, loyalty_status: str):
        """Inserts a new guest into the database."""
        self.cursor.execute('INSERT INTO GUESTS (NAME, EMAIL, PHONE, LOYALTY_STATUS) VALUES (?, ?, ?, ?)',
                            (name, email, phone, loyalty_status))
        self.conn.commit()

    def lookup_guest_by_room(self):
        """Finds and displays guest details and booking history based on room number."""
        room_number = input("Enter room number to look up guest: ")
        try:
            room_id = int(room_number)
            self.cursor.execute('''
                SELECT B.ROOM_ID, G.NAME, G.EMAIL, G.PHONE, G.LOYALTY_STATUS, G.GUEST_ID
                FROM GUESTS G
                JOIN BOOKINGS B ON G.GUEST_ID = B.GUEST_ID
                WHERE B.ROOM_ID = ?
            ''', (room_id,))
            guest = self.cursor.fetchone()
            if guest:
                guest_display = guest[:-1]  # Exclude GUEST_ID
                guest_id = guest[-1]
                headers = ["Room Number", "Name", "Email", "Phone", "Loyalty Status"]
                print(tabulate([guest_display], headers=headers, tablefmt="grid"))

                self.cursor.execute('''
                    SELECT ROOM_ID, CHECK_IN_DATE, CHECK_OUT_DATE
                    FROM BOOKINGS
                    WHERE GUEST_ID = ?
                    ORDER BY CHECK_IN_DATE DESC
                ''', (guest_id,))
                history = self.cursor.fetchall()
                if history:
                    print("\nBooking History:")
                    print(tabulate(history, headers=["Room ID", "Check-in Date", "Check-out Date"], tablefmt="grid"))
                else:
                    print("\nNo booking history found.")
            else:
                print("No guest found for that room.")
        except ValueError:
            print("Invalid room number entered.")

    def update_guest_by_room(self):
        """Updates guest information for a given room number."""
        room_number = input("Enter room number to update guest details: ")
        try:
            room_id = int(room_number)
            self.cursor.execute('''
                SELECT G.GUEST_ID, G.NAME, G.EMAIL, G.PHONE, G.LOYALTY_STATUS
                FROM GUESTS G
                JOIN BOOKINGS B ON G.GUEST_ID = B.GUEST_ID
                WHERE B.ROOM_ID = ?
            ''', (room_id,))
            result = self.cursor.fetchone()
            if result:
                guest_id, name, email, phone, loyalty_status = result
                print("Leave input blank and press Enter to keep current value.")
                new_name = input(f"Name [\033[95m{name}\033[0;0m]: ") or name
                new_email = input(f"Email [\033[95m{email}\033[0;0m]: ") or email
                new_phone = input(f"Phone [\033[95m{phone}\033[0;0m]: ") or phone
                new_loyalty = input(f"Loyalty Status [\033[95m{loyalty_status}\033[0;0m]: ") or loyalty_status

                self.cursor.execute('''
                    UPDATE GUESTS
                    SET NAME = ?, EMAIL = ?, PHONE = ?, LOYALTY_STATUS = ?
                    WHERE GUEST_ID = ?
                ''', (new_name, new_email, new_phone, new_loyalty, guest_id))
                self.conn.commit()
                print("Guest information updated successfully.")
            else:
                print("No guest found for that room.")
        except ValueError:
            print("Invalid room number entered.")

    def create_new_booking(self):
        """Creates a new booking for a guest, inserting new guest if not found."""
        print("\n--- New Booking Form ---")
        name = input("Guest Name: ").strip()
        email = input("Email: ").strip().lower()
        phone = input("Phone (e.g., 05XXXXXXXX): ").strip()

        self.cursor.execute("SELECT GUEST_ID, NAME, EMAIL, PHONE, LOYALTY_STATUS FROM GUESTS WHERE EMAIL = ?", (email,))
        guest = self.cursor.fetchone()

        if guest:
            guest_id, g_name, g_email, g_phone, g_loyalty = guest
            print("\nGuest found:")
            print(tabulate([guest], headers=["Guest ID", "Name", "Email", "Phone", "Loyalty Status"], tablefmt="grid"))
            print("\nThank you for booking again!")
            if g_loyalty.lower() == "bronze":
                print("Eligible for Silver loyalty upgrade!")
            elif g_loyalty.lower() == "silver":
                print("You're close to Gold status!")
            elif g_loyalty.lower() == "gold":
                print("Welcome back, Gold member!")
        else:
            loyalty_status = "Bronze"
            self.insert_guest(name, email, phone, loyalty_status)
            self.cursor.execute("SELECT GUEST_ID FROM GUESTS WHERE EMAIL = ?", (email,))
            guest_id = self.cursor.fetchone()[0]
            print("\nNew guest added with Bronze loyalty status.")

        # Show and select available room
        available_rooms = self.query_rooms_by_status("Available")
        print("\nAvailable Rooms:")
        print(tabulate(available_rooms, headers=["Room ID", "Type", "Amenities", "Price", "Status"], tablefmt="grid"))

        try:
            room_id = int(input("Enter Room ID to book: "))
            check_in = input("Check-in date (YYYY-MM-DD): ")
            check_out = input("Check-out date (YYYY-MM-DD): ")
            self.book_room(guest_id, room_id, check_in, check_out)
            print("\nBooking created successfully!")
        except ValueError:
            print("Invalid room ID or date format.")

    def book_room(self, guest_id: int, room_id: int, check_in: str, check_out: str):
        """Books a room for a guest and updates the room status."""
        self.cursor.execute('''
            INSERT INTO BOOKINGS (GUEST_ID, ROOM_ID, CHECK_IN_DATE, CHECK_OUT_DATE)
            VALUES (?, ?, ?, ?)
        ''', (guest_id, room_id, check_in, check_out))
        self.cursor.execute('UPDATE ROOMS SET STATUS = ? WHERE ID = ?', ('Occupied', room_id))
        self.conn.commit()

    def query_rooms_by_status(self, status: str) -> List[Tuple[int, str, str, float, str]]:
        """Fetches rooms from the database by status."""
        self.cursor.execute('SELECT * FROM ROOMS WHERE STATUS = ?', (status,))
        return self.cursor.fetchall()
