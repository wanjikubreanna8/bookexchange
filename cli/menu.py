from db.connection import session
from models.user import User
from models.book import Book
from models.exchange_request import ExchangeRequest

def show_menu():
    while True:
        print("\n BookExchange CLI")
        print("1. Add user")
        print("2. Add book")
        print("3. View all books")
        print("4. View exchange requests")
        print("5. Add exchange request")
        print("6. Manage incoming requests")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            add_user()
        elif choice == '2':
            add_book()
        elif choice == '3':
            view_books()
        elif choice == '4':
            view_exchange_requests()
        elif choice == '5':
            add_exchange_request()
        elif choice == '6':
            manage_exchange_requests()
        elif choice == '7':
            print(" Goodbye!")
            break
        else:
            print(" Invalid option. Please choose again.")

def add_user():
    name = input("Name: ")
    email = input("Email: ")
    location = input("Location: ")

    user = User(name=name, email=email, location=location)
    session.add(user)
    session.commit()
    print(f" User '{name}' added with ID {user.id}.")

def add_book():
    users = session.query(User).all()
    if not users:
        print(" No users found. Add users first.")
        return

    print(" Users:")
    for u in users:
        print(f"ID: {u.id} | Name: {u.name}")

    title = input("Book title: ")
    author = input("Author: ")
    genre = input("Genre: ")
    try:
        owner_id = int(input("Owner ID: "))
    except ValueError:
        print("Invalid Owner ID.")
        return

    owner = session.query(User).get(owner_id)
    if not owner:
        print(" User not found.")
        return

    book = Book(title=title, author=author, genre=genre, owner_id=owner_id)
    session.add(book)
    session.commit()
    print(f"Book '{title}' added.")

def view_books():
    books = session.query(Book).all()
    if not books:
        print("ℹ o books available.")
        return

    print("\n Available Books:")
    for b in books:
        owner_name = b.owner.name if b.owner else "Unknown"
        print(f"ID: {b.id} | Title: {b.title} | Author: {b.author} | Genre: {b.genre} | Owner: {owner_name}")

def view_exchange_requests():
    requests = session.query(ExchangeRequest).all()
    if not requests:
        print("ℹNo exchange requests found.")
        return

    print("\n Exchange Requests:")
    for r in requests:
        print(
            f"ID: {r.id} | Book: {r.book.title} | Requested by: {r.requester.name} | "
            f"Status: {r.status} | Book Owner: {r.book.owner.name}"
        )

def add_exchange_request():
    users = session.query(User).all()
    books = session.query(Book).all()
    if not users or not books:
        print(" Users or books missing.")
        return

    print("\n Users:")
    for u in users:
        print(f"ID: {u.id} | Name: {u.name}")
    print("\n Books:")
    for b in books:
        print(f"ID: {b.id} | Title: {b.title} | Owner: {b.owner.name}")

    try:
        requester_id = int(input("Your User ID: "))
        book_id = int(input("Book ID to request: "))
    except ValueError:
        print(" Invalid input.")
        return

    requester = session.query(User).get(requester_id)
    book = session.query(Book).get(book_id)

    if not requester or not book:
        print(" User or book not found.")
        return

    if book.owner_id == requester_id:
        print(" You cannot request your own book.")
        return

    request = ExchangeRequest(requester_id=requester_id, book_id=book_id, status="Pending")
    session.add(request)
    session.commit()
    print(f" Request sent to {book.owner.name} for '{book.title}'.")

def manage_exchange_requests():
    print("\n Manage Incoming Exchange Requests")

    try:
        owner_id = int(input("Enter your User ID (book owner): "))
    except ValueError:
        print(" Invalid ID.")
        return

    requests = (
        session.query(ExchangeRequest)
        .join(Book)
        .filter(Book.owner_id == owner_id, ExchangeRequest.status == "Pending")
        .all()
    )

    if not requests:
        print(" No pending requests for your books.")
        return

    print("\n Pending Requests:")
    for r in requests:
        print(
            f"Request ID: {r.id} | Book: {r.book.title} | Requested by: {r.requester.name} | Status: {r.status}"
        )

    while True:
        try:
            request_id = int(input("\nEnter the Request ID to respond to (or 0 to quit): "))
        except ValueError:
            print(" Invalid input.")
            continue

        if request_id == 0:
            print(" Returning to main menu.")
            break

        request = session.query(ExchangeRequest).get(request_id)

        if not request or request.book.owner_id != owner_id or request.status != "Pending":
            print(" Request not found or not available for you.")
            continue

        decision = input("Type 'accept' or 'reject': ").strip().lower()

        if decision == "accept":
            request.status = "Accepted"
            print(" Request accepted.")
        elif decision == "reject":
            request.status = "Rejected"
            print(" Request rejected.")
        else:
            print(" Invalid action. Must be 'accept' or 'reject'.")
            continue

        session.commit()
        print(" Status updated.")
