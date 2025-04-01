import sqlite3
from datetime import date
from roomManagement import Room
from guestManagement import Guest
from paymentInvoicing import Payment
from guestServices import ServiceRequest as GuestServices
from feedbackReviews import Feedback
from inputValidation import Validation
from hotelSystem import Hotel

# Database file name
db_name = 'data.sqlite'

# Connect to the SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Initialize modules
Room = Room(conn=conn)
Guest = Guest(conn=conn)
Payment = Payment(conn=conn)
GuestServices = GuestServices(conn=conn)
Feedback = Feedback(conn=conn)
Hotel = Hotel(Room=Room, Guest=Guest)





if __name__ == "__main__":
    ascii_art = "    ___   ___  ___   _____ ______    _______    ___   ________   ________   ___  ___     \n   |\\  \\ |\\  \\|\\  \\ |\\   _ \\  _   \\ |\\  ___ \\  |\\  \\ |\\   __  \\ |\\   __  \\ |\\  \\|\\  \\    \n   \\ \\  \\\\ \\  \\\\\\  \\\\ \\  \\\\\\__\\ \\  \\\\ \\   __/| \\ \\  \\\\ \\  \\|\\  \\\\ \\  \\|\\  \\\\ \\  \\\\\\  \\   \n __ \\ \\  \\\\ \\  \\\\\\  \\\\ \\  \\\\|__| \\  \\\\ \\  \\_|/__\\ \\  \\\\ \\   _  _\\\\ \\   __  \\\\ \\   __  \\  \n|\\  \\\\_\\  \\\\ \\  \\\\\\  \\\\ \\  \\    \\ \\  \\\\ \\  \\_|\\ \\\\ \\  \\\\ \\  \\\\  \\|\\ \\  \\ \\  \\\\ \\  \\ \\  \\ \n\\ \\________\\\\ \\_______\\\\ \\__\\    \\ \\__\\\\ \\_______\\\\ \\__\\\\ \\__\\\\ _\\ \\ \\__\\ \\__\\\\ \\__\\ \\__\\\n \\|________| \\|_______| \\|__|     \\|__| \\|_______| \\|__| \\|__|\\|__| \\|__|\\|__| \\|__|\\|__|\n ___  ___   ________   _________   _______    ___                                        \n|\\  \\|\\  \\ |\\   __  \\ |\\___   ___\\|\\  ___ \\  |\\  \\                                       \n\\ \\  \\\\\\  \\\\ \\  \\|\\  \\\\|___ \\  \\_|\\ \\   __/| \\ \\  \\                                      \n \\ \\   __  \\\\ \\  \\\\\\  \\    \\ \\  \\  \\ \\  \\_|/__\\ \\  \\                                     \n  \\ \\  \\ \\  \\\\ \\  \\\\\\  \\    \\ \\  \\  \\ \\  \\_|\\ \\\\ \\  \\____                                \n   \\ \\__\\ \\__\\\\ \\_______\\    \\ \\__\\  \\ \\_______\\\\ \\_______\\                              \n    \\|__|\\|__| \\|_______|     \\|__|   \\|_______| \\|_______|                              \n"
    print(ascii_art)
    print("Jumeirah Hotel by Abood")
    print("Best Hotel Ever, Becasue we say so.")

    Hotel.main_menu()