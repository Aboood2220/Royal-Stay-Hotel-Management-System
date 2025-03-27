from datetime import date

class Room:
    """Represents a hotel room with number, type, price, and bookings."""
    def __init__(self, number, room_type, price):
        self.number = number
        self.room_type = room_type
        self.price = price
        self.bookings = []

    def is_available(self, check_in, check_out):
        """Check if the room is available between the given dates."""
        for booking in self.bookings:
            if (check_in < booking.check_out_date and check_out > booking.check_in_date):
                return False
        return True

    def __str__(self):
        """Return a string representation of the room."""
        return f"Room {self.number} ({self.room_type}), ${self.price}/night"

class Guest:
    """Represents a guest with name, contact, and loyalty points."""
    def __init__(self, name, contact):
        self.name = name
        self.contact = contact
        self.points = 0

    def add_points(self, amount):
        """Add loyalty points to the guest's account."""
        self.points += amount

    def use_points(self, amount):
        """Use loyalty points if sufficient are available."""
        if self.points >= amount:
            self.points -= amount
            return True
        return False

    def __str__(self):
        """Return a string representation of the guest."""
        return f"Guest: {self.name}, Points: {self.points}"

class Booking:
    """Represents a booking made by a guest for a room."""
    def __init__(self, guest, room, check_in_date, check_out_date):
        self.guest = guest
        self.room = room
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.room.bookings.append(self)
        self.payment = None

    def __str__(self):
        """Return a string representation of the booking."""
        return f"Booking for {self.guest.name} in Room {self.room.number} from {self.check_in_date} to {self.check_out_date}"

class Payment:
    """Represents a payment for a booking."""
    def __init__(self, booking):
        self.booking = booking
        self.amount = self.calculate_amount()
        self.status = "Pending"

    def calculate_amount(self):
        """Calculate the total amount based on the number of nights."""
        nights = (self.booking.check_out_date - self.booking.check_in_date).days
        return nights * self.booking.room.price

    def pay(self, method):
        """Process the payment and update the status."""
        self.status = f"Paid via {method}"
        self.booking.guest.add_points(int(self.amount))

    def __str__(self):
        """Return a string representation of the payment."""
        return f"Payment for {self.booking}: ${self.amount}, {self.status}"

class ServiceRequest:
    """Represents a service request made by a guest."""
    def __init__(self, guest, request_type):
        self.guest = guest
        self.request_type = request_type
        self.status = "Pending"

    def __str__(self):
        """Return a string representation of the service request."""
        return f"Service Request from {self.guest.name}: {self.request_type} ({self.status})"

class Feedback:
    """Represents feedback for a booking."""
    def __init__(self, booking, rating, comment):
        self.booking = booking
        self.rating = rating
        self.comment = comment

    def __str__(self):
        """Return a string representation of the feedback."""
        return f"Feedback for {self.booking}: Rating {self.rating}/5, Comment: {self.comment}"

class Hotel:
    """Represents the hotel managing rooms, guests, and bookings."""
    def __init__(self):
        self.rooms = []
        self.guests = []
        self.bookings = []

    def add_room(self, room):
        """Add a room to the hotel."""
        self.rooms.append(room)

    def add_guest(self, guest):
        """Add a guest to the hotel."""
        self.guests.append(guest)

    def book_room(self, guest, room, check_in, check_out):
        """Book a room if available and create a payment."""
        if room.is_available(check_in, check_out):
            booking = Booking(guest, room, check_in, check_out)
            self.bookings.append(booking)
            booking.payment = Payment(booking)
            return booking
        else:
            print(f"Error: Room {room.number} is not available.")
            return None

    def process_payment(self, booking, method):
        """Process the payment for a booking."""
        if booking.payment:
            booking.payment.pay(method)

    def add_service_request(self, guest, request_type):
        """Add a service request for a guest."""
        return ServiceRequest(guest, request_type)

    def add_feedback(self, booking, rating, comment):
        """Add feedback for a booking."""
        return Feedback(booking, rating, comment)

if __name__ == "__main__":
    hotel = Hotel()
    room1 = Room(101, "Single", 100)
    room2 = Room(102, "Double", 150)
    hotel.add_room(room1)
    hotel.add_room(room2)
    abdulrahman = Guest("Abdulrahman", "abdulrahman@gmail.com")
    fatima = Guest("Fatima", "fatima@gmail.com")
    hotel.add_guest(abdulrahman)
    hotel.add_guest(fatima)
    booking1 = hotel.book_room(abdulrahman, room1, date(2025, 4, 1), date(2025, 4, 3))
    hotel.process_payment(booking1, "Credit Card")
    booking2 = hotel.book_room(fatima, room2, date(2025, 4, 1), date(2025, 4, 3))
    hotel.process_payment(booking2, "Cash")
    print(booking2.payment)
    print(f"Fatima's points: {fatima.points}")
    print("Abdulrahman tries to use 100 points:", abdulrahman.use_points(100))
    print(f"Abdulrahman's points after: {abdulrahman.points}")
    service = hotel.add_service_request(abdulrahman, "Room Service")
    print(service)
    feedback = hotel.add_feedback(booking1, 5, "Great stay!")
    print(feedback)
