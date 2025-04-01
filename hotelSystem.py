from inputValidation import Validation


class Hotel:
    """Represents the hotel managing rooms, guests, and bookings."""
    def __init__(self, Room, Guest):
        self.Room = Room
        self.Guest = Guest

    def main_menu(self):
        print("\n\033[0;0mAvailable options:\n"
              "\033[95m1.\033[0;0m Rooms\n"
              "\033[95m2.\033[0;0m Bookings\n"
              "\033[95m3.\033[0;0m Guest Services\n"
              "\033[95m4.\033[0;0m Accounting\n"
              "\033[95m5.\033[0;0m Loyalty Programs\n"
              "\033[95m6.\033[0;0m Feedbacks\033[0;0m\n")
        selected_option = input("Select a number: ")
        status, value = Validation.validate_text_input(input_text=selected_option, min_value=1, max_value=6)
        if status == False:
            print(value)
            self.main_menu()
        else:
            print(chr(27) + "[2J")
            match value:
                case 1:
                    # Rooms
                    self.Room.rooms_menu(Hotel=self)
                case 2:
                    # Rooms
                    self.Guest.guest_menu(Hotel=self)
                case 3:
                    # Rooms
                    print("rooms")
                case 4:
                    # Rooms
                    print("rooms")
                case 5:
                    # Rooms
                    print("rooms")
                case 6:
                    # Rooms
                    print("rooms")