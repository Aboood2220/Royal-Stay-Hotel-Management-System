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

# # Create ROOMS table (if it doesn't already exist)
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS ROOMS (
#         ID INTEGER PRIMARY KEY,
#         TYPE TEXT,
#         AMENITIES TEXT,
#         PRICE FLOAT,
#         STATUS TEXT
#     )
# ''')
#
# # Create GUESTS table (if it doesn't already exist)
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS GUESTS (
#         GUEST_ID INTEGER PRIMARY KEY AUTOINCREMENT,
#         NAME TEXT NOT NULL,
#         EMAIL TEXT UNIQUE NOT NULL,
#         PHONE TEXT,
#         LOYALTY_STATUS TEXT,
#         ACCOUNT_CREATED TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#     )
# ''')
#
# # Create BOOKINGS table (if it doesn't already exist)
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS BOOKINGS (
#         BOOKING_ID INTEGER PRIMARY KEY AUTOINCREMENT,
#         GUEST_ID INTEGER NOT NULL,
#         ROOM_ID INTEGER NOT NULL,
#         CHECK_IN_DATE TEXT NOT NULL,
#         CHECK_OUT_DATE TEXT NOT NULL,
#         FOREIGN KEY (GUEST_ID) REFERENCES GUESTS(GUEST_ID),
#         FOREIGN KEY (ROOM_ID) REFERENCES ROOMS(ID)
#     )
# ''')
#
# # Create ACCOUNTING table (if it doesn't already exist)
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS ACCOUNTING (
#         INVOICE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
#         BOOKING_ID INTEGER NOT NULL,
#         NIGHTLY_RATE FLOAT NOT NULL,
#         NUM_NIGHTS INTEGER NOT NULL,
#         ADDITIONAL_CHARGES FLOAT DEFAULT 0.0,
#         DISCOUNTS FLOAT DEFAULT 0.0,
#         TOTAL_AMOUNT FLOAT NOT NULL,
#         PAYMENT_METHOD TEXT NOT NULL,
#         INVOICE_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#         FOREIGN KEY (BOOKING_ID) REFERENCES BOOKINGS(BOOKING_ID)
#     )
# ''')
#
# # Create REQUESTS table (if it doesn't already exist)
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS REQUESTS (
#         REQUEST_ID INTEGER PRIMARY KEY AUTOINCREMENT,
#         GUEST_ID INTEGER NOT NULL,
#         ROOM_ID INTEGER,
#         REQUEST_TYPE TEXT NOT NULL,
#         REQUEST_DESCRIPTION TEXT,
#         STATUS TEXT DEFAULT 'Pending',
#         REQUEST_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#         FOREIGN KEY (GUEST_ID) REFERENCES GUESTS(GUEST_ID),
#         FOREIGN KEY (ROOM_ID) REFERENCES ROOMS(ID)
#     )
# ''')
#
# # Create FEEDBACK table (if it doesn't already exist)
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS FEEDBACK (
#         FEEDBACK_ID INTEGER PRIMARY KEY AUTOINCREMENT,
#         GUEST_ID INTEGER NOT NULL,
#         ROOM_ID INTEGER,
#         RATING INTEGER CHECK(RATING >= 1 AND RATING <= 5),
#         COMMENTS TEXT,
#         SUBMITTED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#         FOREIGN KEY (GUEST_ID) REFERENCES GUESTS(GUEST_ID),
#         FOREIGN KEY (ROOM_ID) REFERENCES ROOMS(ID)
#     )
# ''')

conn.commit()

print("\n--- Generating Random Requests for Guests ---")
cursor.execute('''
    SELECT B.GUEST_ID, B.ROOM_ID
    FROM BOOKINGS B
    LIMIT 15
''')
bookings = cursor.fetchall()

request_types = [
    ("Room Service", (10, 50)),
    ("Housekeeping", (5, 20)),
    ("Laundry", (15, 40)),
    ("Transportation", (20, 100)),
    ("Wake-up Call", (0, 0)),
    ("Spa Appointment", (50, 150))
]

for guest_id, room_id in bookings:
    request_type, (min_fee, max_fee) = random.choice(request_types)
    fee = round(random.uniform(min_fee, max_fee), 2)

    cursor.execute('''
        INSERT INTO REQUESTS (GUEST_ID, ROOM_ID, REQUEST_TYPE, FEE)
        VALUES (?, ?, ?, ?)
    ''', (guest_id, room_id, request_type, fee))

conn.commit()
print("Random request generation complete.")