from inputValidation import Validation


class Hotel:
    """Represents the hotel managing rooms, guests, and bookings."""

    def __init__(self, Room, Guest, GuestServices, Accounting, Feedback):
        self.Room = Room
        self.Guest = Guest
        self.GuestServices = GuestServices
        self.Accounting = Accounting
        self.Feedback = Feedback

    def main_menu(self):
        """Displays the main menu and routes the user to the selected module."""
        print("\n\033[0;0mAvailable options:\n"
              "\033[95m1.\033[0;0m Rooms\n"
              "\033[95m2.\033[0;0m Bookings\n"
              "\033[95m3.\033[0;0m Guest Services\n"
              "\033[95m4.\033[0;0m Accounting\n"
              "\033[95m5.\033[0;0m Feedbacks\033[0;0m\n")

        selected_option = input("Select a number: ")
        status, value = Validation.validate_text_input(input_text=selected_option, min_value=1, max_value=5)

        if not status:
            print(value)
            return self.main_menu()

        print(chr(27) + "[2J")  # Clear screen

        menu_actions = {
            1: self.Room.rooms_menu,
            2: self.Guest.guest_menu,
            3: self.GuestServices.guest_services_menu,
            4: self.Accounting.accounting_menu,
            5: self.Feedback.feedback_menu,
        }

        action = menu_actions.get(value)
        if action:
            action(Hotel=self)