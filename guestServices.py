from typing import List, Tuple
from inputValidation import Validation
from tabulate import tabulate


class ServiceRequest:
    def __init__(self, conn):
        self.cursor = conn.cursor()
        self.conn = conn

    def guest_services_menu(self, Hotel):
        """Displays the guest services menu and handles user input."""
        print("\n\033[0;0mAvailable options:\n"
              "\033[95m1.\033[0;0m House Keeping\n"
              "\033[95m2.\033[0;0m Room Service\n"
              "\033[95m3.\033[0;0m Custom Request\n"
              "\033[95m4.\033[0;0m Main Menu\n")
        selected_option = input("Select a number: ")
        status, value = Validation.validate_text_input(input_text=selected_option, min_value=1, max_value=4)
        if not status:
            print(value)
            return self.guest_services_menu(Hotel)

        actions = {
            1: self.submit_house_keeping_service_request,
            2: self.submit_guest_room_service_request,
            3: self.submit_guest_custom_request,
            4: Hotel.main_menu
        }

        action = actions.get(value)
        if action:
            action() if value == 4 else (action(), self.guest_services_menu(Hotel))

    def get_guest_id_by_room(self, room_id: int) -> int:
        """Fetches the latest guest ID for a given room, or returns None."""
        self.cursor.execute('''
            SELECT G.GUEST_ID FROM BOOKINGS B
            JOIN GUESTS G ON B.GUEST_ID = G.GUEST_ID
            WHERE B.ROOM_ID = ?
            ORDER BY B.CHECK_IN_DATE DESC
            LIMIT 1
        ''', (room_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def submit_guest_custom_request(self):
        """Handles submission of a custom guest service request."""
        print("\n--- Submit Service Request ---")
        room_number = input("Enter room number: ").strip()
        try:
            room_id = int(room_number)
            guest_id = self.get_guest_id_by_room(room_id)
            if not guest_id:
                print("No guest currently associated with that room.")
                return

            request_type = input("Enter request type: ").strip()
            fee_input = input("Enter fee for the request (AED): ").strip()
            try:
                fee = float(fee_input)
            except ValueError:
                fee = 0.0
                print("Invalid fee input, defaulting to 0.0")

            self.cursor.execute('''
                INSERT INTO REQUESTS (GUEST_ID, ROOM_ID, REQUEST_TYPE, FEE)
                VALUES (?, ?, ?, ?)
            ''', (guest_id, room_id, request_type, fee))
            self.conn.commit()
            print("Request submitted successfully.")

        except ValueError:
            print("Invalid room number entered.")

    def submit_guest_room_service_request(self):
        """Submits a pre-defined 'Room Service' request."""
        print("\n--- Submit Room Service Request ---")
        self._submit_standard_request(service_type="Room Service")

    def submit_house_keeping_service_request(self):
        """Submits a pre-defined 'House Keeping' request."""
        print("\n--- Submit House Keeping Request ---")
        self._submit_standard_request(service_type="House Keeping")

    def _submit_standard_request(self, service_type: str):
        """Handles shared logic for submitting predefined service requests."""
        room_number = input("Enter room number: ").strip()
        try:
            room_id = int(room_number)
            guest_id = self.get_guest_id_by_room(room_id)
            if not guest_id:
                print("No guest currently associated with that room.")
                return

            fee_input = input(f"Enter fee for the {service_type} request (AED): ").strip()
            try:
                fee = float(fee_input)
            except ValueError:
                fee = 0.0
                print("Invalid fee input, defaulting to 0.0")

            self.cursor.execute('''
                INSERT INTO REQUESTS (GUEST_ID, ROOM_ID, REQUEST_TYPE, FEE)
                VALUES (?, ?, ?, ?)
            ''', (guest_id, room_id, service_type, fee))
            self.conn.commit()
            print("Request submitted successfully.")

        except ValueError:
            print("Invalid room number entered.")
