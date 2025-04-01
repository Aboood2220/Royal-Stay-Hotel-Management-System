class ServiceRequest:
    def __init__(self, conn):
        self.cursor = conn.cursor()
        self.conn = conn

    # Function to submit a guest service request
    def submit_request(self, guest_id: int, room_id: int, request_type: str, description: str):
        self.cursor.execute('''
            INSERT INTO REQUESTS (GUEST_ID, ROOM_ID, REQUEST_TYPE, REQUEST_DESCRIPTION)
            VALUES (?, ?, ?, ?)
        ''', (guest_id, room_id, request_type, description))
        self.conn.commit()
