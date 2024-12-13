from tkinter import *
from tkinter import ttk
# import mysql.connector
from sampledataset import *

root=Tk()
height=root.winfo_screenheight()
width=root.winfo_screenwidth()

root.geometry(f"{int(width*0.95)}x{int(height*0.95)}")
root.state('zoomed')
root.attributes("-topmost", True)
root.attributes('-fullscreen', True)

paned_window = PanedWindow(root, orient=HORIZONTAL)
paned_window.pack(fill=BOTH, expand=True)

pos_entry_list_frame = Frame(paned_window, background="cadetblue1")
calculation_frame = Frame(paned_window, background="cadetblue3")
product_list_frame = Frame(paned_window, background="cadetblue2")

paned_window.add(pos_entry_list_frame, minsize=width*0.33)
paned_window.add(calculation_frame, minsize=width*0.33)
paned_window.add(product_list_frame)

pos_columns = ("No.", "Name", "Quantity", "Price")

style = ttk.Style()
style.configure("POS.Treeview", font=("Arial", 16), rowheight=30)
style.configure("POS.Treeview.Heading", font=("Arial", 20, "bold"))
style.map("POS.Treeview", background=[("selected", "lightblue")])

style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

style2 = ttk.Style()
style2.configure("PL.Treeview", font=("Arial", 30), rowheight=60)
style2.configure("PL.Treeview.Heading", font=("Arial", 30, "bold"))
style2.map("PL.Treeview", background=[("selected", "lightblue")])

style2.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

pre_pos_frame=Frame(pos_entry_list_frame, background="cadetblue1")
pre_pos_frame.pack(side=TOP,fill=X)

pos_entry_list_treeview = ttk.Treeview(pre_pos_frame, columns=pos_columns, show="headings",height=int(height*0.0231),style="POS.Treeview")
pos_entry_list_treeview.pack(side=LEFT,fill=X)

pos_entry_scrollbar = ttk.Scrollbar(pre_pos_frame, orient="vertical", command=pos_entry_list_treeview.yview)
pos_entry_list_treeview.configure(yscrollcommand=pos_entry_scrollbar.set)
pos_entry_scrollbar.pack(side=LEFT,fill=Y)

pos_entry_list_treeview.column("No.", width=int(width*0.0495), stretch=False)
pos_entry_list_treeview.column("Name", width=int(width*0.1155), stretch=True)
pos_entry_list_treeview.column("Quantity", width=int(width*0.066), stretch=True)
pos_entry_list_treeview.column("Price", width=int(width*0.099), stretch=True)

for col in pos_columns:
    pos_entry_list_treeview.heading(col, text=col)
    pos_entry_list_treeview.column(col, anchor="center")

total_label_frame=LabelFrame(pos_entry_list_frame,text="Total Calculation")
total_label_frame.pack(side=TOP,fill=BOTH,expand=True)

Label(total_label_frame,text="Testing").pack()



product_list_treeview = ttk.Treeview(product_list_frame, columns=('Name','Regional Name','Rate'), show="headings",height=int(height*0.0231),style="PL.Treeview")
product_list_treeview.pack(side=LEFT,fill=X)

product_list_scrollbar = ttk.Scrollbar(product_list_frame, orient="vertical", command=product_list_treeview.yview)
product_list_treeview.configure(yscrollcommand=product_list_scrollbar.set)
product_list_scrollbar.pack(side=LEFT,fill=BOTH,expand=True)

product_list_treeview.column("Name", width=int(width*0.099), stretch=True)
product_list_treeview.column("Regional Name", width=int(width*0.099), stretch=True)
product_list_treeview.column("Rate", width=int(width*0.099), stretch=True)

for col in ('Name','Regional Name','Rate'):
    product_list_treeview.heading(col, text=col)
    product_list_treeview.column(col, anchor="center")

for item in alldata:
    product_list_treeview.insert("", "end", values=(item[1],item[2],item[6]))


def exit_fullscreen(event=None):
    root.attributes('-fullscreen',False)
    root.attributes("-topmost", False)

root.bind("<Escape>", exit_fullscreen)

root.mainloop()