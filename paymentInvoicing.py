from datetime import datetime


class Payment:

    def __init__(self, conn):
        self.cursor = conn.cursor()
        self.conn = conn

    # Function to create invoice upon guest checkout
    def create_invoice(self, booking_id: int, additional_charges: float = 0.0, discounts: float = 0.0,
                       payment_method: str = 'Credit Card'):
        self.cursor.execute('''
            SELECT B.ROOM_ID, B.CHECK_IN_DATE, B.CHECK_OUT_DATE, R.PRICE
            FROM BOOKINGS B
            JOIN ROOMS R ON B.ROOM_ID = R.ID
            WHERE B.BOOKING_ID = ?
        ''', (booking_id,))
        result = self.cursor.fetchone()
        if result:
            room_id, check_in, check_out, nightly_rate = result
            d1 = datetime.strptime(check_in, '%Y-%m-%d')
            d2 = datetime.strptime(check_out, '%Y-%m-%d')
            num_nights = (d2 - d1).days
            total_amount = max((nightly_rate * num_nights + additional_charges - discounts), 0)

            self.cursor.execute('''
                INSERT INTO ACCOUNTING (BOOKING_ID, NIGHTLY_RATE, NUM_NIGHTS, ADDITIONAL_CHARGES, DISCOUNTS, TOTAL_AMOUNT, PAYMENT_METHOD)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (booking_id, nightly_rate, num_nights, additional_charges, discounts, total_amount, payment_method))

            self.cursor.execute('UPDATE ROOMS SET STATUS = ? WHERE ID = ?', ('Available', room_id))
            self.conn.commit()
