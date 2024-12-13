from tkinter import *
from tkinter import messagebox
from tkinter import ttk
# import mysql.connector
from sampledataset import *
from math import floor, ceil
from random import choice

text_box_colors=['#F5F5DC','#FFE4C4','#FFEBCD','#FFF8DC']


class Application(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.height=self.winfo_screenheight()
        self.width=self.winfo_screenwidth()
        self.pos_columns = ("No.", "Name", "Quantity", "Price")
        self.product_list_columns=('Name','Regional Name','Rate')
        
        self.geometry(f"{int(self.width*0.95)}x{int(self.height*0.95)}")
        self.state('zoomed')
        self.attributes("-topmost", True)
        self.attributes('-fullscreen', True)
        
        self.paned_window = PanedWindow(self, orient=HORIZONTAL)
        self.paned_window.pack(fill=BOTH, expand=True)

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

        Label(total_label_frame,text="Testing").pack()

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

        for item in alldata:
            self.insert_row(self.product_list_treeview,(item[1],item[2],item[6]),(item[0],))

        self.entry_string_var = StringVar()

        self.calculation_entry = Entry(calculation_frame, textvariable=self.entry_string_var,font=("Arial",self.font_size(30)),width=int(self.width*0.0145))
        self.calculation_entry.grid(row=0,column=0,columnspan=3,padx=20,pady=20)
        self.entry_string_var.trace_add("write",self.calculation_entry_writer)

        Button(calculation_frame, text='7', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.calculation_button_press("7"), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=1, column=0,pady=10)
        Button(calculation_frame, text='8', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.calculation_button_press("8"), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=1, column=1,pady=10)
        Button(calculation_frame, text='9', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.calculation_button_press("9"), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=1, column=2,pady=10)
        
        Button(calculation_frame, text='4', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.calculation_button_press("4"), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=2, column=0,pady=10)
        Button(calculation_frame, text='5', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.calculation_button_press("5"), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=2, column=1,pady=10)
        Button(calculation_frame, text='6', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.calculation_button_press("6"), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=2, column=2,pady=10)

        Button(calculation_frame, text='1', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.calculation_button_press("1"), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=3, column=0,pady=10)
        Button(calculation_frame, text='2', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.calculation_button_press("2"), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=3, column=1,pady=10)
        Button(calculation_frame, text='3', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.calculation_button_press("3"), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=3, column=2,pady=10)
        
        Button(calculation_frame, text='00', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.calculation_button_press("00"), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=4, column=0,pady=10)
        Button(calculation_frame, text='0', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.calculation_button_press("0"), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=4, column=1,pady=10)
        Button(calculation_frame, text='.', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.calculation_button_press("."), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=4, column=2,pady=10)
        
        Button(calculation_frame, text='Clear', fg='black', bg='#FF7256', font=("Arial",self.font_size(20)), command=self.clear_calculation_entry, height=ceil(self.height*0.0012),width=ceil(self.width*0.004)).grid(row=5, column=0,pady=10)
        Button(calculation_frame, text='+ kg', fg='black', bg='#C1FFC1', font=("Arial", self.font_size(20)), command=lambda: self.add_item_in_pos('kg'),height=ceil(self.height * 0.0012), width=ceil(self.width * 0.004)).grid(row=5, column=1, pady=10)
        Button(calculation_frame, text='+ Gram', fg='black', bg='#C1FFC1', font=("Arial", self.font_size(20)), command=lambda: self.add_item_in_pos('g'),height=ceil(self.height * 0.0012), width=ceil(self.width * 0.004)).grid(row=5, column=2, pady=10)
        
        Button(calculation_frame, text='1 Kg', fg='black', bg='#FFE4B5', font=("Arial",self.font_size(20)), command=lambda: self.add_item_in_pos(1000), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=6, column=0,pady=10)
        Button(calculation_frame, text='750 g', fg='black', bg='#FFDEAD', font=("Arial",self.font_size(20)), command=lambda: self.add_item_in_pos(750), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=6, column=1,pady=10)
        Button(calculation_frame, text='500 g', fg='black', bg='#EECFA1', font=("Arial",self.font_size(20)), command=lambda: self.add_item_in_pos(500), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=6, column=2,pady=10)
        Button(calculation_frame, text='250 g', fg='black', bg='#EECFA1', font=("Arial",self.font_size(20)), command=lambda: self.add_item_in_pos(250), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=7, column=0,pady=10)
        Button(calculation_frame, text='100 g', fg='black', bg='#FFDEAD', font=("Arial",self.font_size(20)), command=lambda: self.add_item_in_pos(100), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=7, column=1,pady=10)
        Button(calculation_frame, text='50 g', fg='black', bg='#FFE4B5', font=("Arial",self.font_size(20)), command=lambda: self.add_item_in_pos(50), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=7, column=2,pady=10)

        Button(calculation_frame, text='Remove', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.add_item_in_pos(100), height=ceil(self.height*0.0012), width=ceil(self.width*0.008)).grid(row=8, column=0,pady=10,columnspan=2)
        Button(calculation_frame, text='Clear', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.add_item_in_pos(50), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=8, column=2,pady=10)

        Button(calculation_frame, text='Print', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.add_item_in_pos(100), height=ceil(self.height*0.0012), width=ceil(self.width*0.008)).grid(row=9, column=0,pady=10,columnspan=2)
        Button(calculation_frame, text='Save', fg='black', bg='#d8c3a5', font=("Arial",self.font_size(20)), command=lambda: self.add_item_in_pos(50), height=ceil(self.height*0.0012), width=ceil(self.width*0.004)).grid(row=9, column=2,pady=10)

        self.bind("<Escape>", self.exit_fullscreen)

    def add_item_in_pos(self,unit):
        value=self.entry_string_var.get()
        product=self.product_list_treeview.selection()
        pos_entries=self.pos_entry_list_treeview.get_children()
        self.product_list_treeview.selection_remove(self.product_list_treeview.selection())
        if value:
            if unit=='kg':
                value=int(value)*1000
            elif unit=="g":
                value=int(value)
        else:
            if unit in ['kg','g']:
                self.calculation_entry.focus_set()
                self.calculation_entry.config(bg=choice(text_box_colors))
                return
            value=unit
        self.clear_calculation_entry()

        if not product:
            messagebox.showwarning(title="No Product Selected",message="Please Select a product to add in cart")
            return
        
        product_details=self.product_list_treeview.item(product[0])["values"]
        product_tags=self.product_list_treeview.item(product[0])["tags"]
        self.insert_row(self.pos_entry_list_treeview,(len(pos_entries)+1,product_details[1],value,product_details[2]),tags=(product_tags[1],))
        
    def calculation_entry_writer(self,*args):
        value = self.entry_string_var.get()
        if not self.is_validate_float_input(value):
            self.entry_string_var.set(value[:-1])
            
    def is_validate_float_input(self,value):
        try:
            if value:
                float(value)
            return True        
        except ValueError:
            return
        
    def clear_calculation_entry(self):
        self.calculation_entry.delete(0,END)
    
    def calculation_button_press(self,value):
        self.calculation_entry.insert(END,value)
        self.calculation_entry_writer()

    def exit_fullscreen(self,event=None):
        self.attributes('-fullscreen',False)
        self.attributes("-topmost", False)

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
        tree.tag_configure("evenrow", background="white")
        tree.tag_configure("oddrow", background="lightgray")

    def insert_row(self,tree:ttk.Treeview,item,tags=()):
        rows = tree.get_children()
        if len(rows)%2==0:
            tree.insert("", "end", values=item, tags=("oddrow",)+tags)
        else:
            tree.insert("", "end", values=item, tags=("evenrow",)+tags)


if __name__ == "__main__":
    app=Application()
    app.mainloop()