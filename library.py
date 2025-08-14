import mysql.connector
from datetime import datetime, timedelta

def get_conn():
    return mysql.connector.connect(
        host="localhost",
        user="root",        # change
        password="password",# change
        database="library_db"
    )

def add_book():
    title = input("Title: ")
    author = input("Author: ")
    with get_conn() as con:
        cur = con.cursor()
        cur.execute("INSERT INTO books(title, author) VALUES(%s,%s)", (title, author))
        con.commit()
        print("Book added.")

def list_books():
    with get_conn() as con:
        cur = con.cursor()
        cur.execute("SELECT id, title, author, available FROM books ORDER BY id")
        for (id_, title, author, available) in cur.fetchall():
            print(f"{id_}	{title}	{author}	{'Yes' if available else 'No'}")

def issue_book():
    uid = int(input("User ID: "))
    bid = int(input("Book ID: "))
    due = datetime.now() + timedelta(days=14)
    with get_conn() as con:
        cur = con.cursor()
        # ensure available
        cur.execute("SELECT available FROM books WHERE id=%s", (bid,))
        row = cur.fetchone()
        if not row or not row[0]:
            print("Book not available.")
            return
        cur.execute("INSERT INTO issues(user_id, book_id, due_date) VALUES(%s,%s,%s)", (uid, bid, due))
        cur.execute("UPDATE books SET available=0 WHERE id=%s", (bid,))
        con.commit()
        print("Issued. Due:", due.strftime("%Y-%m-%d"))

def return_book():
    iid = int(input("Issue ID: "))
    with get_conn() as con:
        cur = con.cursor()
        cur.execute("SELECT book_id FROM issues WHERE id=%s AND returned=0", (iid,))
        row = cur.fetchone()
        if not row:
            print("Issue not found or already returned.")
            return
        bid = row[0]
        cur.execute("UPDATE issues SET returned=1 WHERE id=%s", (iid,))
        cur.execute("UPDATE books SET available=1 WHERE id=%s", (bid,))
        con.commit()
        print("Returned.")

def main():
    print("Library Management (Python + MySQL)")
    while True:
        print("\n1. Add book\n2. List books\n3. Issue book\n4. Return book\n0. Exit")
        ch = input("Choose: ").strip()
        if ch == "1": add_book()
        elif ch == "2": list_books()
        elif ch == "3": issue_book()
        elif ch == "4": return_book()
        elif ch == "0": break
        else: print("Invalid.")

if __name__ == "__main__":
    main()
