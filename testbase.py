import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# Create the main window
root = tk.Tk()
root.title("Treeview Example with Update Feature")
root.geometry("600x400")

# Define columns for the Treeview
columns = ("Product ID", "Name", "Regional Name", "Cost", "MRP", "Rate", "Stock Quantity", "Reorder Level")

# Create the Treeview widget
tree = ttk.Treeview(root, columns=columns, show="headings")

# Define headings for each column
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

# Insert sample data into the Treeview
data = [
    (1, "Tomato", "தக்காளி", 20.50, 25.00, 22.00, 100.500, 50.000),
    (2, "Potato", "உருளைக்கிழங்கு", 15.00, 18.00, 16.50, 200.750, 100.000),
    (3, "Carrot", "கேரட்", 30.00, 35.00, 32.00, 50.000, 25.000),
    (4, "Cucumber", "வெள்ளரி", 10.00, 12.00, 11.00, 150.000, 75.000)
]

# Insert data rows into the Treeview
for item in data:
    tree.insert("", "end", values=item)

# Add a vertical scrollbar to the Treeview
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Pack the Treeview widget
tree.pack(expand=True, fill="both")

# Function to open a message box to edit the stock quantity
def edit_item(event):
    selected_item = tree.selection()
    if selected_item:
        values = tree.item(selected_item)["values"]
        current_stock = values[6]

        # Ask the user to input the new stock quantity using a message box
        new_stock = simpledialog.askfloat("Update Stock Quantity", f"Current stock: {current_stock}\nEnter new stock quantity:")

        if new_stock is not None:
            # Update the treeview item with the new stock value
            updated_values = list(values)
            updated_values[6] = new_stock  # Update stock quantity value
            tree.item(selected_item, values=updated_values)

            # Show a message box confirming the update
            messagebox.showinfo("Update Success", "Stock quantity updated successfully!")

# Bind double-click event on a row to open the edit popup
tree.bind("<Double-1>", edit_item)

# Start the Tkinter event loop
root.mainloop()
