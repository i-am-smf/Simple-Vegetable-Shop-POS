import tkinter as tk

root = tk.Tk()
root.geometry("400x400")

# Container frame for the left widgets
left_container = tk.Frame(root)
left_container.pack(side=tk.LEFT, fill=tk.Y)

# First widget
widget1 = tk.Label(left_container, text="Widget 1", bg="lightblue", width=20, height=5)
widget1.pack(side=tk.TOP, fill=tk.X)

# Second widget
widget2 = tk.Label(left_container, text="Widget 2", bg="lightgreen", width=20, height=5)
widget2.pack(side=tk.TOP, fill=tk.X)

# New widget below the left container (packed below previous widgets)
new_widget = tk.Label(root, text="New Widget Below", bg="pink", width=20, height=5)
new_widget.pack(side=tk.TOP, fill=tk.X)

root.mainloop()
