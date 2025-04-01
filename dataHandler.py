import datetime
import sqlite3
from typing import List, Tuple
import random
from datetime import datetime, timedelta

# Database file name
db_name = 'data.sqlite'

# Connect to the SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Create ROOMS table (if it doesn't already exist)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ROOMS (
        ID INTEGER PRIMARY KEY,
        TYPE TEXT,
        AMENITIES TEXT,
        PRICE FLOAT,
        STATUS TEXT
    )
''')

# Create GUESTS table (if it doesn't already exist)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS GUESTS (
        GUEST_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME TEXT NOT NULL,
        EMAIL TEXT UNIQUE NOT NULL,
        PHONE TEXT,
        LOYALTY_STATUS TEXT,
        ACCOUNT_CREATED TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Create BOOKINGS table (if it doesn't already exist)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS BOOKINGS (
        BOOKING_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        GUEST_ID INTEGER NOT NULL,
        ROOM_ID INTEGER NOT NULL,
        CHECK_IN_DATE TEXT NOT NULL,
        CHECK_OUT_DATE TEXT NOT NULL,
        FOREIGN KEY (GUEST_ID) REFERENCES GUESTS(GUEST_ID),
        FOREIGN KEY (ROOM_ID) REFERENCES ROOMS(ID)
    )
''')

# Create ACCOUNTING table (if it doesn't already exist)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ACCOUNTING (
        INVOICE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        BOOKING_ID INTEGER NOT NULL,
        NIGHTLY_RATE FLOAT NOT NULL,
        NUM_NIGHTS INTEGER NOT NULL,
        ADDITIONAL_CHARGES FLOAT DEFAULT 0.0,
        DISCOUNTS FLOAT DEFAULT 0.0,
        TOTAL_AMOUNT FLOAT NOT NULL,
        PAYMENT_METHOD TEXT NOT NULL,
        INVOICE_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (BOOKING_ID) REFERENCES BOOKINGS(BOOKING_ID)
    )
''')

# Create REQUESTS table (if it doesn't already exist)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS REQUESTS (
        REQUEST_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        GUEST_ID INTEGER NOT NULL,
        ROOM_ID INTEGER,
        REQUEST_TYPE TEXT NOT NULL,
        REQUEST_DESCRIPTION TEXT,
        STATUS TEXT DEFAULT 'Pending',
        REQUEST_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (GUEST_ID) REFERENCES GUESTS(GUEST_ID),
        FOREIGN KEY (ROOM_ID) REFERENCES ROOMS(ID)
    )
''')

# Create FEEDBACK table (if it doesn't already exist)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS FEEDBACK (
        FEEDBACK_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        GUEST_ID INTEGER NOT NULL,
        ROOM_ID INTEGER,
        RATING INTEGER CHECK(RATING >= 1 AND RATING <= 5),
        COMMENTS TEXT,
        SUBMITTED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (GUEST_ID) REFERENCES GUESTS(GUEST_ID),
        FOREIGN KEY (ROOM_ID) REFERENCES ROOMS(ID)
    )
''')

conn.commit()

# Function to go through bookings, calculate totals, and add invoices to the ACCOUNTING table
def generate_accounting_entries():
    cursor.execute('''
        SELECT B.BOOKING_ID, B.ROOM_ID, B.CHECK_IN_DATE, B.CHECK_OUT_DATE, R.PRICE
        FROM BOOKINGS B
        JOIN ROOMS R ON B.ROOM_ID = R.ID
        LEFT JOIN ACCOUNTING A ON B.BOOKING_ID = A.BOOKING_ID
        WHERE A.BOOKING_ID IS NULL
    ''')
    bookings = cursor.fetchall()

    for booking in bookings:
        booking_id, room_id, check_in, check_out, nightly_rate = booking
        try:
            d1 = datetime.strptime(check_in, "%Y-%m-%d")
            d2 = datetime.strptime(check_out, "%Y-%m-%d")
            num_nights = (d2 - d1).days
            additional_charges = 0.0
            discounts = 0.0
            total_amount = max((nightly_rate * num_nights + additional_charges - discounts), 0.0)
            payment_method = "Credit Card"  # Default method for this example

            cursor.execute('''
                INSERT INTO ACCOUNTING (BOOKING_ID, NIGHTLY_RATE, NUM_NIGHTS, ADDITIONAL_CHARGES, DISCOUNTS, TOTAL_AMOUNT, PAYMENT_METHOD)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (booking_id, nightly_rate, num_nights, additional_charges, discounts, total_amount, payment_method))
        except Exception as e:
            print(f"Failed to process booking ID {booking_id}: {e}")

    conn.commit()
    print("Accounting entries generated successfully.")

generate_accounting_entries()

# Close the connection when done
# conn.close()  # Uncomment this if you are done using the database
