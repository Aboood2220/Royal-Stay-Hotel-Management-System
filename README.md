# Jumeirah Hotel Management System

Welcome to the **Jumeirah Hotel Management System**, a comprehensive terminal-based application built in Python. This system supports modular and scalable hotel operations including room and guest management, service requests, invoicing, and feedback collection.

---

## 📁 Project Structure

```
├── main.py                  # Entry point for the application
├── hotelSystem.py           # Central controller coordinating all modules
├── roomManagement.py        # Handles room availability and details
├── guestManagement.py       # Manages guest bookings and guest records
├── paymentInvoicing.py      # Handles invoicing and accounting
├── guestServices.py         # Submits and tracks service requests
├── feedbackReviews.py       # Allows guests to leave feedback and ratings
├── inputValidation.py       # Utility module for validating user input
├── dataHandler.py           # (Utility) Used to populate database and define schema
└── data.sqlite              # SQLite database for persistent storage
```

---

## 🧠 Core Concepts

- **Modularity**: Each major functionality (e.g., Rooms, Guests, Payments) is encapsulated in its own class/module.
- **SQLite Integration**: Data is stored persistently in `data.sqlite`, allowing for a lightweight yet powerful database.
- **Tabulated Display**: `tabulate` is used to format output cleanly in the terminal.
- **Input Validation**: Centralized in `inputValidation.py` to ensure robust user input handling.

---

## 🧭 Application Flow

### `main.py`
- Connects to the database
- Initializes all modules
- Displays an ASCII welcome banner
- Launches the main menu via `Hotel.main_menu()`

### `hotelSystem.py`
- Acts as the controller that links all subsystem modules
- Routes main menu input to the corresponding module

---

## 🛏️ Module Overviews

### `roomManagement.py`
- View available, occupied, or maintenance rooms
- Search room by ID
- Uses status filtering to fetch appropriate records

### `guestManagement.py`
- Create new bookings (adds guest if not present)
- List all guests and lookup by room
- Update guest records
- Automatically handles loyalty statuses (Bronze → Silver → Gold)

### `paymentInvoicing.py`
- Generate final invoice (including stay and service fees)
- Itemized charge breakdown
- Confirms credit card payment and records it in `ACCOUNTING`

### `guestServices.py`
- Request types: Housekeeping, Room Service, Custom
- Assigns request fees
- Links request to current guest based on room

### `feedbackReviews.py`
- Allows guests to submit ratings and comments
- Look up feedback by guest email or room number

### `inputValidation.py`
- Validates if input is a number within a given range
- Used across all modules for menu navigation and form inputs

### `dataHandler.py`
- (Optional utility script)
- Defines the SQLite schema and inserts dummy requests for testing

---

## 📊 UML Class Diagram Description

The system is represented in a UML class diagram with the following class structure and relationships:

### Classes:
- **Hotel**: Central controller; aggregates and coordinates all other modules.
- **Room**: Manages room queries, availability, and display.
- **Guest**: Handles guest creation, lookup, updates, and bookings.
- **Payment**: Manages invoice generation and payment processing.
- **ServiceRequest**: Handles service request submission and tracking.
- **Feedback**: Manages feedback submission and lookup.
- **Validation**: Utility class for input validation used by all modules.

### Relationships:
- `Hotel` **aggregates** `Room`, `Guest`, `Payment`, `ServiceRequest`, and `Feedback`.
- Each of `Room`, `Guest`, `Payment`, `ServiceRequest`, and `Feedback` **uses** `Validation`.
- Methods within each module represent functional operations related to hotel workflows.

This structure ensures separation of concerns and easy maintenance, extension, and testing.

---

## 🧪 Input Validation Examples

The system uses a centralized input validation utility in `inputValidation.py` to ensure all numerical user inputs are safe and within expected ranges.

### Sample Function:
```python
class Validation:
    def validate_text_input(input_text, min_value, max_value):
        try:
            number = float(input_text)
        except ValueError:
            return False, "Input is not a number."

        if not number.is_integer():
            return False, "Number is not a whole number."

        number = int(number)
        if number < min_value or number > max_value:
            return False, f"Number is not within the range {min_value} to {max_value}."

        return True, number
```

### Usage Examples:
- In **Room Menu**:
```python
status, value = Validation.validate_text_input(input_text=selected_option, min_value=1, max_value=5)
```
- In **Guest Menu**:
```python
status, value = Validation.validate_text_input(input_text=selected_option, min_value=1, max_value=6)
```
- In **Feedback Submission**:
```python
rating_input = input("Rate your stay (1-5): ").strip()
# Converted to int and checked in code
```

### Test Case Scenarios:
| Input         | Expected Result                                |
|---------------|-------------------------------------------------|
| `"abc"`       | Invalid: Not a number                           |
| `"4.5"`       | Invalid: Not a whole number                     |
| `"-1"`        | Invalid: Out of range                           |
| `"10"`        | Invalid if menu only allows 1–5                |
| `"2"`         | Valid: returns `(True, 2)`                      |

This approach prevents runtime crashes and provides user-friendly error messages.

---

## 🧪 Technologies Used

- **Python 3.10+**
- **SQLite3**: Embedded database
- **Tabulate**: For pretty-printing tables

---

## ✅ How to Run

```bash
python main.py
```

Make sure you have Python installed and `tabulate` available:
```bash
pip install tabulate
```

---

## 🔧 Extending the Project

- Add GUI support (e.g., Tkinter or PyQt)
- Implement authentication for hotel staff
- Enable CSV/Excel import/export of records
- Add analytics or reporting module

---

## 📜 License

MIT License. Feel free to use, modify, and distribute with credit.

---

## 👤 Author

Developed by **Abood** as part of a hotel automation project. Contributions are welcome!

