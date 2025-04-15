import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import json

def create_table():                                                            # Database setup
    con = sqlite3.connect("admin_data.db")
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )  
    ''')
    con.commit()
    con.close()

def insert_admin_data(username, password):
    con = sqlite3.connect("admin_data.db")
    cur = con.cursor()
    try:
        cur.execute('INSERT INTO admin (username, password) VALUES (?, ?)', (username, password))
        con.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        con.close()

def validate_login(username, password):
    con = sqlite3.connect("admin_data.db")
    cur = con.cursor()
    cur.execute('SELECT * FROM admin WHERE username = ? AND password = ?', (username, password))
    result = cur.fetchone()
    con.close()
    return result is not None

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("PAAJI'S ")
        self.root.geometry("800x600")
        self.root.configure(bg="#F0F2F5")            # Light background for Facebook theme
        create_table()                                                # Create the table if it doesn't exist
        self.show_welcome_page()                         # Show the welcome page first
        self.report_window = None                         # Initialize the report window referenc
        self.inventory_window = None                   # Initialize the inventory window reference
        self.restaurant_window = None                 # Initialize the restaurant window reference
    def show_welcome_page(self):                      # Create a welcome frame
        self.welcome_frame = tk.Frame(self.root, bg="#F0F2F5", padx=20, pady=20)
        self.welcome_frame.pack(fill="both", expand=True)
        self.logo_image = tk.PhotoImage(file="logo paaji's.png")  # Load the logo image
        logo_label = tk.Label(self.welcome_frame, image=self.logo_image, bg="#F0F2F5")
        logo_label.pack(side=tk.TOP, pady=10)    # Position the logo at the top center
        tk.Label(self.welcome_frame, text="Welcome to Paaji's Management System", font=("Helvetica", 26), bg="#F0F2F5", fg="#3b5998").pack(pady=20)
        tk.Button(self.welcome_frame, text="Proceed to Login", command=self.show_login_page, bg="#3b5998", fg="white", font=("Helvetica Bold", 16), padx=20, pady=10, borderwidth=2, relief="raised").pack(pady=10)

    def show_login_page(self):                   # Hide welcome frame and show login frame
        self.welcome_frame.pack_forget()  # Remove the welcome frame
        self.create_login_widgets()              # Create and show login widgets

    def create_login_widgets(self):
        self.login_frame = tk.Frame(self.root, bg="#FFFFFF", padx=20, pady=20, relief="groove", borderwidth=2)
        self.login_frame.pack(pady=100)

        tk.Label(self.login_frame, text="Username:", bg="#FFFFFF", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self.login_frame, font=("Helvetica", 12))
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.login_frame, text="Password:", bg="#FFFFFF", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*", font=("Helvetica", 12))
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.login_frame, text="Login", command=self.login, bg="#3b5998", fg="white", font=("Helvetica Bold", 12), padx=20, pady=5, borderwidth=2, relief="raised").grid(row=2, columnspan=2, pady=10)
        tk.Button(self.login_frame, text="Sign Up", command=self.show_signup, bg="#3b5998", fg="white", font=("Helvetica Bold", 12), padx=20, pady=5, borderwidth=2, relief="raised").grid(row=3, columnspan=2, pady=5)

    def show_signup(self):                                                   # Hide login frame and show signup frame
        for widget in self.login_frame.winfo_children():
            widget.destroy()                                                     # Remove all widgets from the login frame

        tk.Label(self.login_frame, text ="Username:", bg="#FFFFFF", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.signup_username_entry = tk.Entry(self.login_frame, font=("Helvetica", 12))
        self.signup_username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.login_frame, text="Password:", bg="#FFFFFF", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=5)
        self.signup_password_entry = tk.Entry(self.login_frame, show="*", font=("Helvetica", 12))
        self.signup_password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.login_frame, text="Register", command=self.register_admin, bg="#3b5998", fg="white", font=("Helvetica Bold", 12), padx=20, pady=5, borderwidth=2, relief="raised").grid(row=2, columnspan=2, pady=10)
        tk.Button(self.login_frame, text="Back to Login", command=self.show_login, bg="#FF5722", fg="white", font=("Helvetica Bold", 12), padx=20, pady=5, borderwidth=2, relief="raised").grid(row=3, columnspan=2, pady=5)

    def show_login(self):                                                             # Hide signup frame and show login frame
        for widget in self.login_frame.winfo_children():
            widget.destroy()                                                            # Remove all widgets from the signup frame

        tk.Label(self.login_frame, text="Username:", bg="#FFFFFF", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self.login_frame, font=("Helvetica", 12))
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.login_frame, text="Password:", bg="#FFFFFF", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*", font=("Helvetica", 12))
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.login_frame, text="Login", command=self.login, bg="#3b5998", fg="white", font=("Helvetica Bold", 12), padx=20, pady=5, borderwidth=2, relief="raised").grid(row=2, columnspan=2, pady=10)
        tk.Button(self.login_frame, text="Sign Up", command=self.show_signup, bg="#3b5998", fg="white", font=("Helvetica Bold", 12), padx=20, pady=5, borderwidth=2, relief="raised").grid(row=3, columnspan=2, pady=5)

    def register_admin(self):
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get()
        if username and password:
            if insert_admin_data(username, password):
                messagebox.showinfo("Success", "Admin registered successfully!")
                self.show_login()
            else:
                messagebox.showerror("Error", "Username already exists. Please choose a different username.")
        else:
            messagebox.showwarning("Warning", "Please fill in both fields.")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if validate_login(username, password):
            messagebox.showinfo("Success", "Login successful!")
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid credentials. Please try again.")

    def show_main_menu(self):
        for widget in self.login_frame.winfo_children():
            widget.destroy()                                                        # Remove all widgets from the login frame
        self.login_frame.pack_forget()
        self.create_main_menu()                                              # Create and show main menu

    def create_main_menu(self):
        self.main_menu_frame = tk.Frame(self.root, bg="#F0F2F5")
        tk.Label(self.main_menu_frame, text="Welcome To The Admin Dashboard", font=("Helvetica", 26), bg="#F0F2F5", fg="#3b5998").pack(pady=20)
        tk.Label(self.main_menu_frame, text="Select an option to proceed", font=("Helvetica", 20), bg="#F0F2F5", fg="#3b5998").pack(pady=20)
        tk.Button(self.main_menu_frame, text="Inventory Management", command=self.open_inventory_system, width=30, height=2, font=("Helvetica Bold", 16), bg="#3b5998", fg="white", borderwidth=2, relief="raised").pack(pady=10)
        tk.Button(self.main_menu_frame, text="Billing System", command=self.open_restaurant_system, width=30, height=2, font=("Helvetica Bold", 16), bg="#3b5998", fg="white", borderwidth=2, relief="raised").pack(pady=10)
        tk.Button(self.main_menu_frame, text="Report App Issues", command=self.open_report_issues_window, width=30, height=2, font=("Helvetica Bold", 16), bg="#3b5998", fg="white", borderwidth=2, relief="raised").pack(pady=10)  # Updated button color
        tk.Button(self.main_menu_frame, text="Log Out", command=self.sign_out, width=30, height=2, font=("Helvetica Bold", 16), bg="#3b5998", fg="white", borderwidth=2, relief="raised").pack(pady=10)  # Keep the Log Out button as is
        self.main_menu_frame.pack(fill="both", expand=True)   # Show main menu frame

    def open_report_issues_window(self):
        if self.report_window is not None and self.report_window.winfo_exists():
            self.report_window.lift()                                        # Bring the existing window to the front
            return                                                                      # Exit the method if the window is already open

        self.report_window = tk.Toplevel(self.root)
        self.report_window.title("Report App Issues")
        self.report_window.geometry("400x300")
        self.report_window.configure(bg="#F0F2F5")

        tk.Label(self.report_window, text="Describe the issue:", font=("Helvetica", 14), bg="#F0F2F5", fg="#3b5998").pack(pady=10)

        self.issue_text = tk.Text(self.report_window, height=10, width=40, font=("Helvetica", 12))
        self.issue_text.pack(pady=10)

        tk.Button(self.report_window, text="Submit", command=self.submit_issue, bg="#3b5998", fg="white", font=("Helvetica Bold", 12), borderwidth=2, relief="raised").pack(pady=10)
        tk.Button(self.report_window, text="Cancel", command=self.close_report_window, bg="#FF5722", fg="white", font=("Helvetica Bold", 12), borderwidth=2, relief="raised").pack(pady=5)
        self.root.wait_window(self.report_window)      # Wait for the report window to close before returning to the main application
        
    def close_report_window(self):
        self.report_window.destroy()           # Close the report window
        self.report_window = None               # Reset the reference
        
    def submit_issue(self):
        issue = self.issue_text.get("1.0", tk.END).strip()  # Get the text from the Text widget
        if issue:                                                                       # Here you can implement the logic to save the issue, e.g., to a file or database
            messagebox.showinfo("Success", "Your issue has been reported successfully!")
            self.issue_text.delete("1.0", tk.END)                  # Clear the text area
        else:
            messagebox.showwarning("Warning", "Please describe the issue before submitting.")

    def sign_out(self):
        self.root.destroy()
    
    def open_inventory_system(self):                    # Check if the inventory window is already open
        if self.inventory_window is not None and self.inventory_window.winfo_exists():
            self.inventory_window.lift()                      # Bring the existing window to the front
            return                                                          # Exit the method if the window is already open
        self.inventory_window = tk.Toplevel(self.root)
        IApp(self.inventory_window)                      

    def open_restaurant_system(self):                # Check if the restaurant window is already open
        if self.restaurant_window is not None and self.restaurant_window.winfo_exists():
            self.restaurant_window.lift()                   # Bring the existing window to the front
            return                                                         # Exit the method if the window is already open
        self.restaurant_window = tk.Toplevel(self.root)
        RestaurantManagementSystem(self.restaurant_window)
class IApp:                                                             # Inventory Management System
    def __init__(self, root):
        self.root = root
        self.root.title("PAAJI'S Inventory Management System")
        self.root.geometry("800x600")
        self.root.configure(bg='#F0F2F5')
        self.items = {}
        self.file_path = "grocery_data.json"
        self.create_widgets()
        self.load_items()

    def create_widgets(self):
        # Frame for entry fields
        entry_frame = tk.LabelFrame(self.root, text="Product Details")
        entry_frame.pack(padx=15, pady=10, fill="x")
        # Labels and Entry fields
        tk.Label(entry_frame, text="Item Name:", font=("Times New Roman", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Label(entry_frame, text="Quantity:", font=("Times New Roman", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Label(entry_frame, text="Price:", font=("Times New Roman", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.item_name = tk.Entry(entry_frame, width=40, borderwidth=2, relief="solid", font=("Helvetica", 12))
        self.item_name.grid(row=0, column=1, padx=10, pady=5)
        self.quantity = tk.Entry(entry_frame, width=40, borderwidth=2, relief="solid", font=("Helvetica", 12))
        self.quantity.grid(row=1, column=1, padx=10, pady=5)
        self.price = tk.Entry(entry_frame, width=40, borderwidth=2, relief="solid", font=("Helvetica", 12))
        self.price.grid(row=2, column=1, padx=10, pady=5)

        # Frame for buttons and search input
        button_frame = tk.LabelFrame(self.root, bg='#ffffff', padx=20, pady=10, text="Tools")
        button_frame.pack(padx=15, pady=10, fill="x")

        # Buttons with modern design
        btn_config = {"font": ("Helvetica", 12), "padx": 10, "pady": 5, "width": 14, "bd": 0, "relief": "flat"}
        tk.Button(button_frame, text="Add Item", command=self.add_item, bg='#4CAF50', fg='#ffffff', **btn_config).grid(row=1, column=0)
        tk.Button(button_frame, text="Delete Item", command=self.delete_item, bg='#f44336', fg='#ffffff', **btn_config).grid(row=1, column=1)
        tk.Button(button_frame, text="Update Item", command=self.update_item, bg='#2196F3', fg='#ffffff', **btn_config).grid(row=1, column=2)
        tk.Button(button_frame, text="Show Items", command=self.show_items, bg='#FF5722', fg='#ffffff', **btn_config).grid(row=2, column=2)

        # Search entry and button
        tk.Label(button_frame, text="Search:", bg='#ffffff', font=("Helvetica", 14)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.search_entry = tk.Entry(button_frame, width=20, borderwidth=2, relief="solid", font=("Helvetica", 12))
        self.search_entry.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(button_frame, text="Search", command=self.search_item, bg='#FFC107', fg='#ffffff', **btn_config).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(button_frame, text="Save", command=self.save_items, bg='#8BC34A', fg='#ffffff', **btn_config).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Load", command=self.load_items, bg='#3F51B5', fg='#ffffff', **btn_config).grid(row=2, column=1, padx=5, pady=5)

        # Frame for Treeview
        tree_frame = tk.LabelFrame(self.root, bg='#ffffff', padx=10, pady=10, text="Product list")
        tree_frame.pack(padx=15, pady=10, fill="both", expand=True)

        # Treeview for displaying items
        self.tree = ttk.Treeview(tree_frame, columns=("Name", "Quantity", "Price"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price")
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Bind Treeview selection event to on_treeview_select
        self.tree.bind("<<TreeviewSelect>>", self.on_treeview_select)

        # Scrollbars
        self.v_scroll = tk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=self.v_scroll.set)
        self.h_scroll = tk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.h_scroll.grid(row=1, column=0, sticky="ew")
        self.tree.configure(xscrollcommand=self.h_scroll.set)

        # Expandable rows and columns
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

    def add_item(self):
        name = self.item_name.get()
        quantity = self.quantity.get()
        price = self.price.get()
        if name and quantity and price:
            self.items[name] = (quantity, price)
            self.clear_entries()
            self.show_items()
            messagebox.showinfo("Info", f"Item '{name}' added successfully!")
        else:
            messagebox.showwarning("Warning", "Please fill all fields!")

    def delete_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_name = self.tree.item(selected_item)['values'][0]
            if item_name in self.items:
                del self.items[item_name]
                self.clear_entries()
                self.show_items()
                messagebox.showinfo("Info", f"Item '{item_name}' deleted successfully!")
            else:
                messagebox.showwarning("Warning", "Item not found!")
        else:
            messagebox.showwarning("Warning", "Please select an item to delete!")

    def update_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_name = self.tree.item(selected_item)['values'][0]
            new_quantity = self.quantity.get()
            new_price = self.price.get()
            if new_quantity and new_price:
                if item_name in self.items:
                    self.items[item_name] = (new_quantity, new_price)
                    self.clear_entries()
                    self.show_items()
                    messagebox.showinfo("Info", f"Item '{item_name}' updated successfully!")
                else:
                    messagebox.showwarning("Warning", "Item not found!")
            else:
                messagebox.showwarning("Warning", "Please enter new quantity and price!")
        else:
            messagebox.showwarning("Warning", "Please select an item to update!")

    def show_items(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for name, (quantity, price) in self.items.items():
            self.tree.insert("", "end", values=(name, quantity, price))

    def search_item(self):
        search_term = self.search_entry.get().lower()
        self.tree.delete(*self.tree.get_children())
        item_found = False
        for name, (quantity, price) in self.items.items():
            if search_term in name.lower():
                self.tree.insert("", "end", values=(name, quantity, price))
                item_found = True

    def save_items(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.items, f)
        messagebox.showinfo("Info", "Items saved successfully!")

    def load_items(self):
        try:
            with open(self.file_path, 'r') as f:
                self.items = json.load(f)
            self.show_items()
        except FileNotFoundError:
            messagebox.showwarning("Warning", "No saved data found.")

    def clear_entries(self):
        self.item_name.delete(0, tk.END)
        self.quantity.delete(0, tk.END)
        self.price.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)

    def on_treeview_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_name = self.tree.item(selected_item)['values'][0]
            quantity, price = self.items.get(item_name, ('', ''))
            self.item_name.delete(0, tk.END)
            self.item_name.insert(0, item_name)
            self.quantity.delete(0, tk.END)
            self.quantity.insert(0, quantity)
            self.price.delete(0, tk.END)
            self.price.insert(0, price)

class RestaurantManagementSystem:  # Restaurant Management System
    def __init__(self, root):
        self.root = root
        self.root.title("PAAJI'S Restaurant Management System")
        self.customer_name = tk.StringVar()
        self.customer_email = tk.StringVar()
        self.customer_contact = tk.StringVar()
        self.items = {
            "Burger": 100,
            "Pizza": 200,
            "Pasta": 150,
            "Manchurian": 80,
            "Spring Roll": 90
        }
        self.orders = {}
        self.gst_percentage = 18
        self.create_gui()

    def create_gui(self):
        details_frame = tk.LabelFrame(self.root, text="Customer Details")
        details_frame.pack(fill="x", padx=10, pady=10)
        name_label = tk.Label(details_frame, text="Name:")
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        name_entry = tk.Entry(details_frame, textvariable=self.customer_name)
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        email_label = tk.Label(details_frame, text="Email:")
        email_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        email_entry = tk.Entry(details_frame, textvariable=self.customer_email)
        email_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        contact_label = tk.Label(details_frame, text="Contact:")
        contact_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        contact_entry = tk.Entry(details_frame, textvariable=self.customer_contact)
        contact_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        contact_entry.configure(validate="key")
        contact_entry.configure(validatecommand=(contact_entry.register(self.validate_contact), "%P"))

        menu_frame = tk.LabelFrame(self.root, text="Menu")
        menu_frame.pack(fill="both", expand=True, padx=10, pady=10)
        item_header = tk.Label(menu_frame, text="Items")
        item_header.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        quantity_header = tk.Label(menu_frame, text="Quantity")
        quantity_header.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        row = 1
        for item, price in self.items.items():
            item_var = tk.IntVar()
            item_label = tk.Label(menu_frame, text=f"{item} - {self.convert_to_inr(price)}")
            item_label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
            quantity_entry = tk.Entry(menu_frame, width=5)
            quantity_entry.grid(row=row, column=1, padx=5, pady=5, sticky="w")
            self.orders[item] = {"var": item_var, "quantity": quantity_entry}
            row += 1

        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        print_bill_button = tk.Button(buttons_frame, text="Print Bill", command=self.show_bill_popup)
        print_bill_button.pack(side="left", padx=5)
        past_record_button = tk.Button(buttons_frame, text="Past Records", command=self.past_records)
        past_record_button.pack(side="left", padx=5)
        clear_selection_button = tk.Button(buttons_frame, text="Clear Selection", command=self.clear_selection)
        clear_selection_button.pack(side="left", padx=5)
        self.sample_bill_text = tk.Text(self.root, height=10)
        self.sample_bill_text.pack(fill="x", padx=10, pady=10)

        # Update sample bill when quantity or item is selected
        for item, info in self.orders.items():
            info["quantity"].bind("<FocusOut>", lambda event, item=item: self.update_sample_bill(item))
            info["quantity"].bind("<Return>", lambda event, item=item: self.update_sample_bill(item))
            info["quantity"].bind("<KeyRelease>", lambda event, item=item: self.update_sample_bill(item))
            info["var"].trace("w", lambda *args, item=item: self.update_sample_bill(item))

    def show_bill_popup(self):
        # Check if customer name is provided
        if not self.customer_name.get().strip():
            messagebox.showwarning("Warning", "Please enter customer name.")
            return
        selected_items = []
        total_price = 0
        for item, info in self.orders.items():
            quantity = info["quantity"].get()
            if quantity:
                selected_items.append((item, int(quantity)))
                total_price += self.items[item] * int(quantity)
        if not selected_items:
            messagebox.showwarning("Warning", "Please select at least one item.")
            return
        gst_amount = (total_price * self.gst_percentage) / 100
        bill = f"Customer Name: {self.customer_name.get()}\n"
        bill += f"Customer email: {self.customer_email.get()}\n"
        bill += f"Customer Contact: {self.customer_contact.get()}\n\n"
        bill += "Selected Items:\n"
        for item, quantity in selected_items:
            bill += f"{item} x {quantity} - {self.convert_to_inr(self.items[item] * quantity)}\n"
        bill += f"\nTotal Price: {self.convert_to_inr(total_price)}\n"
        bill += f"GST ({self.gst_percentage}%): {self.convert_to_inr(gst_amount)}\n"
        bill += f"Grand Total: {self.convert_to_inr(total_price + gst_amount)}"
        messagebox.showinfo("Bill", bill)

    def past_records(self):
        messagebox.showinfo("Past Records", "This feature is not implemented yet.")

    def clear_selection(self):
        for item, info in self.orders.items():
            info["var"].set(0)
            info["quantity"].delete(0, tk.END)

    def update_sample_bill(self, item):
        selected_items = []
        total_price = 0
        for item, info in self.orders.items():
            quantity = info["quantity"].get()
            if quantity:
                selected_items.append((item, int(quantity)))
                total_price += self.items[item] * int(quantity)
        gst_amount = (total_price * self.gst_percentage) / 100
        bill = f"Customer Name: {self.customer_name.get()}\n"
        bill += f"Customer email: {self.customer_email.get()}\n"
        bill += f"Customer Contact: {self.customer_contact.get()}\n\n"
        bill += "Selected Items:\n"
        for item, quantity in selected_items:
            bill += f"{item} x {quantity} - {self.convert_to_inr(self.items[item] * quantity)}\n"
        bill += f"\nTotal Price: {self.convert_to_inr(total_price)}\n"
        bill += f"GST ({self.gst_percentage}%): {self.convert_to_inr(gst_amount)}\n"
        bill += f"Grand Total: {self.convert_to_inr(total_price + gst_amount)}"
        self.sample_bill_text.delete("1.0", tk.END)  # Clear previous contents
        self.sample_bill_text.insert(tk.END, bill)

    def validate_contact(self, value):
        return value.isdigit() or value == ""

    @staticmethod
    def convert_to_inr(amount):
        return "₹" + str(amount)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
