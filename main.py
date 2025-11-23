from datetime import datetime, timedelta
import os

class DuplicateVisitorError(Exception):
    pass

class EarlyEntryError(Exception):
    pass

FILENAME = "visitors.txt"

def ensure_file():
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w") as f:
            pass

def get_last_visitor():
    if not os.path.exists(FILENAME):
        return None, None

    with open(FILENAME, "r") as f:
        lines = f.readlines()

    if not lines:
        return None, None

    last_line = lines[-1].strip()
    name, time_str = last_line.split(",")
    last_time = datetime.fromisoformat(time_str)
    return name, last_time

def add_visitor(visitor_name):
    last_name, last_time = get_last_visitor()
    now = datetime.now()

    if last_name == visitor_name:
        raise DuplicateVisitorError("This visitor was already logged last time!")

    if last_time and (now - last_time) < timedelta(minutes=5):
        raise EarlyEntryError("Visitors must wait 5 minutes before next entry!")

    with open(FILENAME, "a") as f:
        f.write(f"{visitor_name},{now.isoformat()}\n")

def main():
    ensure_file()
    name = input("Enter visitor's name: ")
    try:
        add_visitor(name)
        print("Visitor added successfully!")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
