data = [
    (1, "தக்காளி", 1, 50.000),
    (2, "உருளைக்கிழங்கு", 1, 100.000),
    (3, "கேரட்", 1, 25.000),
    (4, "வெள்ளரி", 1, 75.000)
]

for index, item in enumerate(data):
    if index % 2 == 0:
        pos_entry_list_treeview.insert("", "end", values=item, tags=("evenrow",))
    else:
        pos_entry_list_treeview.insert("", "end", values=item, tags=("oddrow",))

pos_entry_list_treeview.tag_configure("evenrow", background="white")
pos_entry_list_treeview.tag_configure("oddrow", background="lightgray")
