from tkinter import Tk,PanedWindow,LabelFrame,Label,StringVar,Entry,Button,Frame,HORIZONTAL,BOTH,TOP,X,LEFT,Y,END
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from math import ceil,floor
from random import choice
import sqlite3

text_box_colors=['#F5F5DC','#FFE4C4','#FFEBCD','#FFF8DC']

product_table_query='''
CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) DEFAULT 'VEG',
    regional_name VARCHAR(100) DEFAULT 'காய்கறி',
    product_description VARCHAR(255) DEFAULT NULL,
    cost DECIMAL(10, 2) NOT NULL DEFAULT 1.00,
    mrp DECIMAL(10, 2) NOT NULL DEFAULT 1.00,
    rate DECIMAL(10, 2) NOT NULL DEFAULT 1.00,
    unit_price DECIMAL(10, 2) NOT NULL DEFAULT 1.00,
    stock_quantity DECIMAL(10, 3) NOT NULL DEFAULT 0.000,
    reorder_level DECIMAL(10, 3) NOT NULL DEFAULT 0.000,
    added_date DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
'''
sales_table_query='''
CREATE TABLE IF NOT EXISTS sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    sale_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    discount DECIMAL(10, 2) DEFAULT 0.00,
    net_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    sale_items JSON NOT NULL
);'''

sqlite3_query='''
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT DEFAULT 'VEG',
    regional_name TEXT DEFAULT 'காய்கறி',
    product_description TEXT DEFAULT NULL,
    cost REAL NOT NULL DEFAULT 1.00,
    mrp REAL NOT NULL DEFAULT 1.00,
    rate REAL NOT NULL DEFAULT 1.00,
    unit_price REAL NOT NULL DEFAULT 1.00,
    stock_quantity REAL NOT NULL DEFAULT 0.000,
    reorder_level REAL NOT NULL DEFAULT 0.000,
    added_date DATETIME DEFAULT CURRENT_TIMESTAMP
);'''

sqlite3_query2='''
CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount REAL NOT NULL DEFAULT 0.00,
    discount REAL DEFAULT 0.00,
    net_amount REAL NOT NULL DEFAULT 0.00,
    sale_items TEXT NOT NULL
);'''

class Database:
    def __init__(self):
        type=self.db_connection()
        self.check_tables(type)

    def db_connection(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="smfsql123",
                database="vegetableshop"
            )
            self.cursor=self.connection.cursor()
            return 'mysql'
            
        except:
            self.connection = sqlite3.connect('vegetableshop.db')
            self.cursor = self.connection.cursor()
            return 'sqlite3'

    def refresh_cursor(self):
        try: 
            self.connection.close()
        except:
            pass
        self.db_connection()

        try:
            self.cursor.close()
        except:
            pass
        self.cursor=self.connection.cursor()

    def check_tables(self,type):
        if type == "mysql":
            self.cursor.execute(product_table_query)
            self.refresh_cursor()
            self.cursor.execute(sales_table_query)
        else:
            self.cursor.execute(sqlite3_query)
            self.refresh_cursor()
            self.cursor.execute(sqlite3_query2)
    
    def all_products(self):
        self.cursor.execute('select * from products;')
        result = self.cursor.fetchall()
        return result

    def product_view_tree_data(self):
        self.cursor.execute('select product_id, product_name, regional_name, rate from products;')
        result = self.cursor.fetchall()
        return result

    def get_product_rate(self,product_id):
        self.cursor.execute(f'select rate from products where product_id = {product_id};')
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:return False

db=Database()

class Application(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.height=self.winfo_screenheight()
        self.width=self.winfo_screenwidth()
        self.pos_columns = ("No.", "Name", "Quantity", "Price")
        self.product_list_columns=('Name','Regional Name','Rate')
        
        self.geometry(f"{int(self.width*0.95)}x{int(self.height*0.95)}")
        self.state('zoomed')
        self.enter_fullscreen()
        
        self.paned_window = PanedWindow(self, orient=HORIZONTAL)
        self.paned_window.pack(fill=BOTH, expand=True)
        
        menu=Menu(self)
        self.config(menu=menu)
        file_menu=Menu(menu)
        menu.add_cascade(label="Menu",menu=file_menu)
        file_menu.add_command(label="Admin Menu",command=self.paned_window.pack_forget)
        file_menu.add_command(label="POS",command=self.show_pos)
        file_menu.add_separator()
        file_menu.add_command(label="Refresh Products",command=self.refresh_all_products)
        file_menu.add_separator()
        file_menu.add_command(label="Enter Full Screen",command=self.enter_fullscreen)
        file_menu.add_command(label="Exit Full Screen",command=self.exit_fullscreen)
        file_menu.add_separator()
        file_menu.add_command(label="Exit",command=self.quit)

        self.admin_frame = Frame(self, background="cadetblue1")
        self.admin_frame.pack(fill=BOTH, expand=True)

        pos_entry_list_frame = Frame(self.paned_window, background="cadetblue1")
        calculation_frame = Frame(self.paned_window, background="cadetblue3")
        product_list_frame = Frame(self.paned_window, background="cadetblue2")

        self.paned_window.add(pos_entry_list_frame, minsize=self.width*0.336)
        self.paned_window.add(calculation_frame, minsize=self.width*0.33)
        self.paned_window.add(product_list_frame, minsize=self.width*0.33)

        style = ttk.Style()
        style.configure("POS.Treeview", font=("Arial", self.font_size(16)), rowheight=self.get_height(30))
        style.configure("POS.Treeview.Heading", font=("Arial", self.font_size(20), "bold"))
        style.map("POS.Treeview", background=[("selected", "lightblue")])

        style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

        style2 = ttk.Style()
        style2.configure("PL.Treeview", font=("Arial", self.font_size(20)), rowheight=self.get_height(60))
        style2.configure("PL.Treeview.Heading", font=("Arial", self.font_size(30), "bold"))
        style2.map("PL.Treeview", background=[("selected", "lightblue")])

        style2.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

        self.cart_id=Entry(pos_entry_list_frame,font=('Arial',self.font_size(15)),borderwidth=2,background="#FDF5E6",foreground="#000080",state=DISABLED)
        self.cart_id.pack(side=TOP,fill=X)

        pre_pos_frame=Frame(pos_entry_list_frame, background="cadetblue1")
        pre_pos_frame.pack(side=TOP,fill=X)

        self.pos_entry_list_treeview = ttk.Treeview(pre_pos_frame, columns=self.pos_columns, show="headings",height=(int(self.height*0.0231)),style="POS.Treeview")
        self.pos_entry_list_treeview.pack(side=LEFT,fill=X)
        self.tree_rows_configure(self.pos_entry_list_treeview)

        pos_entry_scrollbar = ttk.Scrollbar(pre_pos_frame, orient="vertical", command=self.pos_entry_list_treeview.yview)
        self.pos_entry_list_treeview.configure(yscrollcommand=pos_entry_scrollbar.set)
        pos_entry_scrollbar.pack(side=LEFT,fill=Y)

        self.pos_entry_list_treeview.column("No.", width=int(self.width*0.0495), stretch=False)
        self.pos_entry_list_treeview.column("Name", width=int(self.width*0.1155), stretch=True)
        self.pos_entry_list_treeview.column("Quantity", width=int(self.width*0.066), stretch=True)
        self.pos_entry_list_treeview.column("Price", width=int(self.width*0.099), stretch=True)

        self.center_tree_column(self.pos_entry_list_treeview,self.pos_columns)

        total_label_frame=LabelFrame(pos_entry_list_frame,text="Total Calculation")
        total_label_frame.pack(side=TOP,fill=BOTH,expand=True)

        total_weight_label=Label(total_label_frame,text="Total Weight:",font=('Arial',self.font_size(15)))
        total_weight_label.grid(row=0,column=0,padx=20,pady=10)

        self.total_weight_label=Label(total_label_frame,text="0.000 Kg",font=('Arial',self.font_size(30)),background="#F5FFFA",foreground="#C0FF3E")
        self.total_weight_label.grid(row=0,column=1,sticky=W,pady=10)

        total_amount_label=Label(total_label_frame,text="Total Amount:",font=('Arial',self.font_size(15)))
        total_amount_label.grid(row=1,column=0,pady=10,padx=20)

        self.total_amount_label=Label(total_label_frame,text="₹ 00.00",font=('Arial',self.font_size(38)),background="#FDF5E6",foreground="#FF0000")
        self.total_amount_label.grid(row=1,column=1,pady=10,sticky=W)

        self.product_list_treeview = ttk.Treeview(product_list_frame, columns=self.product_list_columns, show="headings",height=int(self.height*0.0231),style="PL.Treeview",selectmode="browse")
        self.product_list_treeview.pack(side=LEFT,fill=X)
        self.tree_rows_configure(self.product_list_treeview)

        product_list_scrollbar = ttk.Scrollbar(product_list_frame, orient="vertical", command=self.product_list_treeview.yview)
        self.product_list_treeview.configure(yscrollcommand=product_list_scrollbar.set)
        product_list_scrollbar.pack(side=LEFT,fill=BOTH,expand=True)

        self.product_list_treeview.column("Name", width=int(self.width*0.099), stretch=True)
        self.product_list_treeview.column("Regional Name", width=int(self.width*0.099), stretch=True)
        self.product_list_treeview.column("Rate", width=int(self.width*0.099), stretch=True)

        self.center_tree_column(self.product_list_treeview,self.product_list_columns)

        for item in db.product_view_tree_data():
            self.insert_row(self.product_list_treeview,(item[1],item[2],item[3]),(item[0],))

        self.entry_string_var = StringVar()

        self.calculation_entry = Entry(calculation_frame, textvariable=self.entry_string_var,font=("Arial",self.font_size(30)),width=int(self.width*0.0145))
        self.calculation_entry.grid(row=0,column=0,columnspan=3,padx=20,pady=20)
        self.entry_string_var.trace_add("write",self.calculation_entry_writer)

        Button(calculation_frame, text='7', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.calculation_button_press("7"), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=1, column=0,pady=5)
        Button(calculation_frame, text='8', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.calculation_button_press("8"), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=1, column=1,pady=5)
        Button(calculation_frame, text='9', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.calculation_button_press("9"), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=1, column=2,pady=5)
        
        Button(calculation_frame, text='4', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.calculation_button_press("4"), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=2, column=0,pady=5)
        Button(calculation_frame, text='5', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.calculation_button_press("5"), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=2, column=1,pady=5)
        Button(calculation_frame, text='6', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.calculation_button_press("6"), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=2, column=2,pady=5)

        Button(calculation_frame, text='1', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.calculation_button_press("1"), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=3, column=0,pady=5)
        Button(calculation_frame, text='2', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.calculation_button_press("2"), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=3, column=1,pady=5)
        Button(calculation_frame, text='3', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.calculation_button_press("3"), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=3, column=2,pady=5)
        
        Button(calculation_frame, text='00', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.calculation_button_press("00"), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=4, column=0,pady=5)
        Button(calculation_frame, text='0', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.calculation_button_press("0"), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=4, column=1,pady=5)
        Button(calculation_frame, text='.', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.calculation_button_press("."), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=4, column=2,pady=5)
        
        Button(calculation_frame, text='Clear', fg='black', bg='#FF7256', font=("Arial",self.font_size(20)), command=self.clear_calculation_entry, height=ceil(self.height*0.0012),width=ceil(self.width*0.004)).grid(row=5, column=0,pady=5)
        Button(calculation_frame, text='+ kg', fg='black', bg='#C1FFC1', font=("Arial", self.font_size(20)), command=lambda: self.add_item_in_pos('kg'),height=ceil(self.height * 0.0012), width=ceil(self.width * 0.004)).grid(row=5, column=1, pady=5)
        Button(calculation_frame, text='+ Gram', fg='black', bg='#C1FFC1', font=("Arial", self.font_size(20)), command=lambda: self.add_item_in_pos('g'),height=ceil(self.height * 0.0012), width=ceil(self.width * 0.004)).grid(row=5, column=2, pady=5)
        
        Button(calculation_frame, text='1 Kg', fg='black', bg='#FFE4B5', font=("Arial",self.font_size(20)), command=lambda: self.add_item_in_pos(1000), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=6, column=0,pady=10)
        Button(calculation_frame, text='750 g', fg='black', bg='#FFDEAD', font=("Arial",self.font_size(20)), command=lambda: self.add_item_in_pos(750), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=6, column=1,pady=10)
        Button(calculation_frame, text='500 g', fg='black', bg='#EECFA1', font=("Arial",self.font_size(20)), command=lambda: self.add_item_in_pos(500), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=6, column=2,pady=10)
        Button(calculation_frame, text='250 g', fg='black', bg='#EECFA1', font=("Arial",self.font_size(20)), command=lambda: self.add_item_in_pos(250), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=7, column=0,pady=10)
        Button(calculation_frame, text='100 g', fg='black', bg='#FFDEAD', font=("Arial",self.font_size(20)), command=lambda: self.add_item_in_pos(100), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=7, column=1,pady=10)
        Button(calculation_frame, text='50 g', fg='black', bg='#FFE4B5', font=("Arial",self.font_size(20)), command=lambda: self.add_item_in_pos(50), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=7, column=2,pady=10)

        Button(calculation_frame, text='Remove', fg='black', bg='#FF7256', font=("Arial",self.font_size(20)), command=self.remove_item_in_pos, height=ceil(self.height*0.0012), width=ceil(self.width*0.006)).grid(row=8, column=0,pady=10,columnspan=2,sticky="W",padx=40)
        Button(calculation_frame, text='Refresh', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=self.clear_cart, height=ceil(self.height*0.0012), width=ceil(self.width*0.006)).grid(row=8, column=1,pady=10,columnspan=2,sticky="E",padx=40)

        Button(calculation_frame, text='Print', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.add_item_in_pos(100), height=ceil(self.height*0.0012), width=ceil(self.width*0.006)).grid(row=9, column=0,pady=10,columnspan=2,sticky="W",padx=40)
        Button(calculation_frame, text='Save', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.add_item_in_pos(50), height=ceil(self.height*0.0012), width=ceil(self.width*0.006)).grid(row=9, column=1,pady=10,columnspan=2,sticky="E",padx=40)

        self.bind("<Escape>", self.exit_fullscreen)
        self.bind("<F11>", self.enter_fullscreen)

    def refresh_all_products(self):
        db.refresh_cursor()
        for i in self.product_list_treeview.get_children():
            self.product_list_treeview.delete(i)

        for item in db.product_view_tree_data():
            self.insert_row(self.product_list_treeview,(item[1],item[2],item[3]),(item[0],))
        
        messagebox.showwarning(title="Refresh Products",message="Refreshed all products.")

    def add_item_in_pos(self,unit):
        value=self.entry_string_var.get()
        product=self.product_list_treeview.selection()
        pos_entries=self.pos_entry_list_treeview.get_children()
        self.product_list_treeview.selection_remove(self.product_list_treeview.selection())
        if value and unit in ['kg','g']:
            if unit=='kg':
                value=float(value)*1000
            elif unit=="g":
                value=float(value)
        else:
            if unit in ['kg','g']:
                self.calculation_entry.focus_set()
                self.calculation_entry.config(bg=choice(text_box_colors))
                return
            value=float(unit)
        self.clear_calculation_entry()

        if not product:
            messagebox.showwarning(title="No Product Selected",message="Please Select a product to add to cart.")
            return
        
        product_details=self.product_list_treeview.item(product[0])["values"]
        product_id=self.product_list_treeview.item(product[0])["tags"][1]
        rate = float(db.get_product_rate(product_id))
        if rate:
            self.insert_row(self.pos_entry_list_treeview,(len(pos_entries)+1,product_details[1],value,value*rate/1000),tags=(product_id,))
        self.update_calculation_frame()
        
    def remove_item_in_pos(self):
        product=self.pos_entry_list_treeview.selection()
        if not product:
            messagebox.showwarning(title="No Product Selected",message="Please Select a product to remove from cart.")
            return
        self.pos_entry_list_treeview.delete(product)
        self.pos_entry_list_treeview.selection_remove(self.pos_entry_list_treeview.selection())
        pos_entries=self.pos_entry_list_treeview.get_children()
        for i,j in enumerate(pos_entries):
            values=self.pos_entry_list_treeview.item(j)["values"]
            self.pos_entry_list_treeview.item(j, values=(i+1,values[1],values[2],values[3]))
        self.update_calculation_frame()

    def update_calculation_frame(self):
        total_weight=0
        total_amount=0
        for i in self.pos_entry_list_treeview.get_children():
            values=self.pos_entry_list_treeview.item(i)["values"]
            total_weight+=float(values[2])
            total_amount+=float(values[3])

        self.total_amount_label.config(text=f"₹ {self.format_to_money(floor(total_amount))}")
        self.total_weight_label.config(text=f"{total_weight/1000} Kg")

    def clear_cart(self):
        yesno=messagebox.askokcancel(title="Clear Cart",message="Are you want to clear the cart?")
        if yesno:
            for i in self.pos_entry_list_treeview.get_children():
                self.pos_entry_list_treeview.delete(i)

        self.total_amount_label.config(text=f"₹ 0.00")
        self.total_weight_label.config(text=f"0.000 Kg")

    def calculation_entry_writer(self,*args):
        while True:
            value = self.entry_string_var.get()
            if not self.is_validate_float_input(value):
                self.entry_string_var.set(value[:-1])
            else:
                break
    def show_pos(self):
        self.paned_window.pack(fill=BOTH, expand=True)

    def is_validate_float_input(self,value):
        try:
            if value:
                float(value)
            return True
        except ValueError:
            return
    def format_to_money(self,number):
        num_str = str(number).split(".")
        
        integer_part = num_str[0]
        integer_part_with_commas = "{:,}".format(int(integer_part))
        
        if len(num_str) > 1:
            return f"{integer_part_with_commas}.{num_str[1]}"
        return integer_part_with_commas

    def clear_calculation_entry(self):
        self.calculation_entry.delete(0,END)
    
    def calculation_button_press(self,value):
        self.calculation_entry.insert(END,value)
        self.calculation_entry_writer()

    def exit_fullscreen(self,event=None):
        self.attributes('-fullscreen',False)
        self.attributes("-topmost", False)

    def enter_fullscreen(self,event=None):
        self.attributes('-fullscreen',True)
        self.attributes("-topmost", True)

    def center_tree_column(self,tree:ttk.Treeview,columns:tuple):
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

    def font_size(self,value):
        return ceil(self.height * (value * 100 / self.height) / 100)
    
    def get_height(self,value):
        return ceil(self.height * (value * 100 / self.height) / 100)

    def get_width(self,value):
        return ceil(self.width * (value * 100 / self.width) / 100)
    
    def tree_rows_configure(self,tree:ttk.Treeview):
        pass
        # tree.tag_configure("evenrow", background="white")
        # tree.tag_configure("oddrow", background="lightgray")

    def insert_row(self,tree:ttk.Treeview,item,tags=()):
        rows = tree.get_children()
        if len(rows)%2==0:
            tree.insert("", "end", values=item, tags=("oddrow",)+tags)
        else:
            tree.insert("", "end", values=item, tags=("evenrow",)+tags)


# if __name__ == "__main__":
app=Application()
app.mainloop()