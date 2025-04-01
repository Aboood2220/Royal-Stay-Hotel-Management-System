class Feedback:
    def __init__(self, conn):
        self.cursor = conn.cursor()
        self.conn = conn

    # Function to submit feedback after stay
    def submit_feedback(self, guest_id: int, room_id: int, rating: int, comments: str):
        self.cursor.execute('''
            INSERT INTO FEEDBACK (GUEST_ID, ROOM_ID, RATING, COMMENTS)
            VALUES (?, ?, ?, ?)
        ''', (guest_id, room_id, rating, comments))
        self.conn.commit()
