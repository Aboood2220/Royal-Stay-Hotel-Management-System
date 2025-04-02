from typing import List, Tuple
from inputValidation import Validation
from tabulate import tabulate


class Feedback:
    def __init__(self, conn):
        self.cursor = conn.cursor()
        self.conn = conn

    def feedback_menu(self, Hotel):
        """Displays the feedback menu and routes user selection."""
        print("\n\033[0;0mAvailable options:\n"
              "\033[95m1.\033[0;0m Submit Feedback\n"
              "\033[95m2.\033[0;0m Lookup Feedback by Email\n"
              "\033[95m3.\033[0;0m Lookup Feedback by Room\n"
              "\033[95m4.\033[0;0m Main Menu\n")
        selected_option = input("Select a number: ")
        status, value = Validation.validate_text_input(input_text=selected_option, min_value=1, max_value=4)

        if not status:
            print(value)
            return self.feedback_menu(Hotel)

        actions = {
            1: self.submit_feedback,
            2: self.lookup_feedback_by_email,
            3: self.lookup_feedback_by_room,
            4: Hotel.main_menu
        }

        action = actions.get(value)
        if action:
            action() if value == 4 else (action(), self.feedback_menu(Hotel))

    def submit_feedback(self):
        """Allows a guest to submit feedback about a room or stay."""
        print("\n--- Submit Feedback ---")
        room_number = input("Enter room number: ").strip()
        try:
            room_id = int(room_number)
            self.cursor.execute('''
                SELECT G.GUEST_ID, G.NAME FROM BOOKINGS B
                JOIN GUESTS G ON B.GUEST_ID = G.GUEST_ID
                WHERE B.ROOM_ID = ?
                ORDER BY B.CHECK_IN_DATE DESC
                LIMIT 1
            ''', (room_id,))
            result = self.cursor.fetchone()

            if not result:
                print("No guest currently associated with that room.")
                return

            guest_id, guest_name = result
            print(f"Guest: {guest_name}")
            rating_input = input("Rate your stay (1-5): ").strip()
            try:
                rating = int(rating_input)
                if not 1 <= rating <= 5:
                    raise ValueError
            except ValueError:
                print("Invalid rating. Must be an integer between 1 and 5.")
                return

            comments = input("Leave your comments: ").strip()

            self.cursor.execute('''
                INSERT INTO FEEDBACK (GUEST_ID, ROOM_ID, RATING, COMMENTS)
                VALUES (?, ?, ?, ?)
            ''', (guest_id, room_id, rating, comments))
            self.conn.commit()
            print("Thank you for your feedback!")

        except ValueError:
            print("Invalid room number entered.")

    def lookup_feedback_by_email(self):
        """Fetches and displays all feedback submitted by a guest via email."""
        print("\n--- Lookup Feedback by Email ---")
        email = input("Enter guest email address: ").strip().lower()
        self.cursor.execute('''
            SELECT G.NAME, G.EMAIL, F.ROOM_ID, F.RATING, F.COMMENTS, F.SUBMITTED_AT
            FROM FEEDBACK F
            JOIN GUESTS G ON F.GUEST_ID = G.GUEST_ID
            WHERE G.EMAIL = ?
            ORDER BY F.SUBMITTED_AT DESC
        ''', (email,))
        feedback_entries = self.cursor.fetchall()

        if feedback_entries:
            headers = ["Name", "Email", "Room ID", "Rating", "Comments", "Submitted At"]
            print(tabulate(feedback_entries, headers=headers, tablefmt="grid"))
        else:
            print("No feedback found for that email.")

    def lookup_feedback_by_room(self):
        """Fetches and displays all feedback associated with a room."""
        print("\n--- Lookup Feedback by Room Number ---")
        room_number = input("Enter room number: ").strip()
        try:
            room_id = int(room_number)
            self.cursor.execute('''
                SELECT G.NAME, G.EMAIL, F.ROOM_ID, F.RATING, F.COMMENTS, F.SUBMITTED_AT
                FROM FEEDBACK F
                JOIN GUESTS G ON F.GUEST_ID = G.GUEST_ID
                WHERE F.ROOM_ID = ?
                ORDER BY F.SUBMITTED_AT DESC
            ''', (room_id,))
            feedback_entries = self.cursor.fetchall()

            if feedback_entries:
                headers = ["Name", "Email", "Room ID", "Rating", "Comments", "Submitted At"]
                print(tabulate(feedback_entries, headers=headers, tablefmt="grid"))
            else:
                print("No feedback found for that room number.")
        except ValueError:
            print("Invalid room number entered.")
