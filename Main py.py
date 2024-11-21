import tkinter as tk
from tkinter import ttk, messagebox

rooms = {101: {"type": "Single", "price": 100, "status": "Available"},
         102: {"type": "Double", "price": 150, "status": "Available"},
         103: {"type": "Suite", "price": 250, "status": "Available"}}


def update_table(filter_status=None):
    table.delete(*table.get_children())
    for num, info in rooms.items():
        if not filter_status or info["status"] == filter_status:
            table.insert("", "end", values=(num, info["type"], f"${info['price']}", info["status"]))


def handle_room(action):
    try:
        num = int(room_num.get())
        if num not in rooms:
            return messagebox.showerror("Error", "Room not found.")
        if action == "book":
            name = cust_name.get()
            if rooms[num]["status"] == "Available":
                rooms[num]["status"] = f"Booked by {name}"
                messagebox.showinfo("Success", f"Room {num} booked for {name}.")
            else:
                raise ValueError("Room already booked.")
        elif action == "checkout":
            if "Booked" in rooms[num]["status"]:
                rooms[num]["status"] = "Available"
                messagebox.showinfo("Success", f"Room {num} is now available.")
            else:
                raise ValueError("Room is not booked.")
        update_table()
    except ValueError as e:
        messagebox.showerror("Error", str(e))


def add_room():
    try:
        num = int(add_num.get())
        rtype = add_type.get()
        price = float(add_price.get())
        if num in rooms:
            return messagebox.showerror("Error", "Room already exists.")
        rooms[num] = {"type": rtype, "price": price, "status": "Available"}
        update_table()
        add_window.destroy()
    except ValueError:
        messagebox.showerror("Error", "Enter valid room details.")


def open_add_window():
    global add_window, add_num, add_type, add_price
    add_window = tk.Toplevel(app)
    add_window.geometry("300x200")
    tk.Label(add_window, text="Room Number").grid(row=0, column=0, padx=5, pady=5)
    add_num = tk.Entry(add_window)
    add_num.grid(row=0, column=1, padx=5, pady=5)
    tk.Label(add_window, text="Room Type").grid(row=1, column=0, padx=5, pady=5)
    add_type = tk.Entry(add_window)
    add_type.grid(row=1, column=1, padx=5, pady=5)
    tk.Label(add_window, text="Price").grid(row=2, column=0, padx=5, pady=5)
    add_price = tk.Entry(add_window)
    add_price.grid(row=2, column=1, padx=5, pady=5)
    tk.Button(add_window, text="Add Room", command=add_room).grid(row=3, column=0, columnspan=2, pady=10)


# Main Application
app = tk.Tk()
app.title("Hotel Management")
app.geometry("700x400")

tk.Label(app, text="Hotel Management System", font=("Arial", 16)).pack(pady=10)

frame = tk.Frame(app)
frame.pack(pady=10)

tk.Label(frame, text="Customer Name").grid(row=0, column=0, padx=5, pady=5)
cust_name = tk.Entry(frame)
cust_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Room Number").grid(row=1, column=0, padx=5, pady=5)
room_num = tk.Entry(frame)
room_num.grid(row=1, column=1, padx=5, pady=5)

btn_frame = tk.Frame(app)
btn_frame.pack(pady=10)

buttons = [
    ("View All Rooms", lambda: update_table()),
    ("Book Room", lambda: handle_room("book")),
    ("Check Out", lambda: handle_room("checkout")),
    ("Available Rooms", lambda: update_table("Available")),
    ("Add Room", open_add_window),
]

for i, (text, cmd) in enumerate(buttons):
    tk.Button(btn_frame, text=text, command=cmd).grid(row=0, column=i, padx=5)

cols = ("Room", "Type", "Price", "Status")
table = ttk.Treeview(app, columns=cols, show="headings")
for col in cols:
    table.heading(col, text=col)
    table.column(col, anchor="center")
table.pack(fill=tk.BOTH, expand=True, pady=10)

update_table()
app.mainloop()
