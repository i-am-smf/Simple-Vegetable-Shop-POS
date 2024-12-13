import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()
root.title("Treeview Example")
root.geometry("600x400")

# Define columns for the Treeview
columns = ("Product ID", "Name", "Regional Name", "Cost", "MRP", "Rate", "Stock Quantity", "Reorder Level")

# Create the Treeview widget
tree = ttk.Treeview(root, columns=columns, show="headings",selectmode="extended")

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

# Add a button to delete selected item
def delete_item():
    selected_item = tree.selection()
    if selected_item:
        tree.delete(selected_item)

delete_button = tk.Button(root, text="Delete Selected", command=delete_item)
delete_button.pack(pady=10)

# Add a button to add a new row
def add_item():
    new_item = (5, "Onion", "சரக்கு", 22.00, 26.00, 24.00, 120.500, 60.000)
    tree.insert("", "end", values=new_item)

add_button = tk.Button(root, text="Add Item", command=add_item)
add_button.pack(pady=10)

# Function to update a selected item
def update_item():
    selected_item = tree.selection()
    
    for i in selected_item:
        
        tree.item(i, values=("6", "Beans", "பீன்ஸ்", "40.00", "45.00", "42.00", "80.500", "40.000"))

update_button = tk.Button(root, text="Update Selected", command=update_item)
update_button.pack(pady=10)



# Start the Tkinter event loop
root.mainloop()
