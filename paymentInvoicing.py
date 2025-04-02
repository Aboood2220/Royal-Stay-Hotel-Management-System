from datetime import datetime
from inputValidation import Validation
from tabulate import tabulate


class Payment:
    def __init__(self, conn):
        self.cursor = conn.cursor()
        self.conn = conn

    def accounting_menu(self, Hotel):
        """Displays the accounting menu and handles user input."""
        print("\n\033[0;0mAvailable options:\n"
              "\033[95m1.\033[0;0m Generate Invoice\n"
              "\033[95m2.\033[0;0m Guest Charges\n"
              "\033[95m3.\033[0;0m Main Menu\n")
        selected_option = input("Select a number: ")
        status, value = Validation.validate_text_input(input_text=selected_option, min_value=1, max_value=3)
        if not status:
            print(value)
            return self.accounting_menu(Hotel)

        actions = {
            1: self.generate_final_invoice,
            2: self.display_itemized_invoice,
            3: Hotel.main_menu
        }

        action = actions.get(value)
        if action:
            action() if value == 3 else (action(), self.accounting_menu(Hotel))

    def generate_final_invoice(self):
        """Generates and displays the final invoice for a guest and records payment."""
        print("\n--- Generate Final Invoice ---")
        room_number = input("Enter room number: ").strip()
        try:
            room_id = int(room_number)
            self.cursor.execute('''
                SELECT B.BOOKING_ID, G.GUEST_ID, R.PRICE, B.CHECK_IN_DATE, B.CHECK_OUT_DATE
                FROM BOOKINGS B
                JOIN ROOMS R ON B.ROOM_ID = R.ID
                JOIN GUESTS G ON B.GUEST_ID = G.GUEST_ID
                WHERE B.ROOM_ID = ?
                ORDER BY B.CHECK_IN_DATE DESC
                LIMIT 1
            ''', (room_id,))
            booking = self.cursor.fetchone()

            if not booking:
                print("No booking found for that room.")
                return

            booking_id, guest_id, nightly_rate, check_in, check_out = booking
            num_nights = (datetime.strptime(check_out, "%Y-%m-%d") - datetime.strptime(check_in, "%Y-%m-%d")).days
            stay_total = nightly_rate * num_nights

            self.cursor.execute('''
                SELECT SUM(FEE) FROM REQUESTS
                WHERE ROOM_ID = ? AND GUEST_ID = ?
            ''', (room_id, guest_id))
            request_fees = self.cursor.fetchone()[0] or 0.0
            total_due = stay_total + request_fees

            invoice_data = [[
                f"AED {nightly_rate:.2f} x {num_nights} nights = AED {stay_total:.2f}",
                f"Additional Requests = AED {request_fees:.2f}",
                f"TOTAL DUE = AED {total_due:.2f}"
            ]]
            print("\nFinal Invoice:")
            print(tabulate(invoice_data, headers=["Room Charges", "Service Charges", "Total"], tablefmt="grid"))

            confirm = input("Proceed with credit card payment? (yes/no): ").strip().lower()
            if confirm == "yes":
                self.cursor.execute('''
                    INSERT INTO ACCOUNTING (BOOKING_ID, NIGHTLY_RATE, NUM_NIGHTS, ADDITIONAL_CHARGES, DISCOUNTS, TOTAL_AMOUNT, PAYMENT_METHOD)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (booking_id, nightly_rate, num_nights, request_fees, 0.0, total_due, "Credit Card"))
                self.conn.commit()
                print("\nPayment successful. Invoice saved.")
            else:
                print("\nPayment cancelled.")

        except ValueError:
            print("Invalid room number entered.")

    def display_itemized_invoice(self):
        """Displays itemized charges for a guest's stay including services used."""
        print("\n--- Itemized Invoice ---")
        room_number = input("Enter room number: ").strip()
        try:
            room_id = int(room_number)
            self.cursor.execute('''
                SELECT B.BOOKING_ID, G.GUEST_ID, R.PRICE, B.CHECK_IN_DATE, B.CHECK_OUT_DATE
                FROM BOOKINGS B
                JOIN ROOMS R ON B.ROOM_ID = R.ID
                JOIN GUESTS G ON B.GUEST_ID = G.GUEST_ID
                WHERE B.ROOM_ID = ?
                ORDER BY B.CHECK_IN_DATE DESC
                LIMIT 1
            ''', (room_id,))
            booking = self.cursor.fetchone()

            if not booking:
                print("No booking found for that room.")
                return

            booking_id, guest_id, nightly_rate, check_in, check_out = booking
            num_nights = (datetime.strptime(check_out, "%Y-%m-%d") - datetime.strptime(check_in, "%Y-%m-%d")).days
            stay_total = nightly_rate * num_nights

            self.cursor.execute('''
                SELECT REQUEST_TYPE, FEE FROM REQUESTS
                WHERE ROOM_ID = ? AND GUEST_ID = ?
            ''', (room_id, guest_id))
            requests = self.cursor.fetchall()

            print("\nRoom Charges:")
            room_charges = [[f"Night {i + 1}", f"AED {nightly_rate:.2f}"] for i in range(num_nights)]
            print(tabulate(room_charges, headers=["Description", "Amount"], tablefmt="grid"))

            print("\nService Charges:")
            if requests:
                print(tabulate(requests, headers=["Service", "Fee"], tablefmt="grid"))
            else:
                print("No service charges found.")

            request_fees = sum(fee for _, fee in requests) if requests else 0.0
            total_due = stay_total + request_fees

            print("\nTotal Due:")
            summary = [["Room Charges", f"AED {stay_total:.2f}"],
                       ["Service Charges", f"AED {request_fees:.2f}"],
                       ["Total Amount", f"AED {total_due:.2f}"]]
            print(tabulate(summary, tablefmt="grid"))

        except ValueError:
            print("Invalid room number entered.")
