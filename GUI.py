import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from NTFS import *
from FAT32 import *
from MBR import *
#from test import *


root = tk.Tk()
root.title("Operating System Project")
treeview1 = ttk.Treeview(root)  # Tạo cây thứ nhất
treeview2 = ttk.Treeview(root)  # Tạo cây thứ hai

file_icon = tk.PhotoImage(file="file.png") # Dùng để chèn icon
folder_icon = tk.PhotoImage(file="folder.png") # Dùng để chèn icon

treeview1.tag_configure('custom_font', font=('Arial', 14))
treeview2.tag_configure('custom_font', font=('Arial', 14))



def set_window_to_fullscreen(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}")

def get_data_by_key(data_list, key):
    # Initialize an empty list to store matching values
    matching_values = []
    
    # Iterate over each dictionary in the list
    for item in data_list:
        # Check if the key exists in the dictionary
        if key in item:
            # If the key exists, append the corresponding value to the list
            matching_values.append(item)
    
    # Return the list of matching values
    return matching_values

def show_disk_info_1(file_system, item):
    new_item = treeview1.selection()[0]
    new_item1 = get_data_by_key(u, new_item)[0][new_item]
    item2 = calculate_file_size(new_item1)
    if (get_data_by_key(u, new_item)[0]["type"] == -1 ):
        item1 = calculate_folder_size(new_item1)
        messagebox.showinfo("NTFS Information", f"This volume is a NTFS32 folder system\n This is a folder\n Folder system size: {item1} bytes")
        return
    item3 = FAT32_date(new_item1)
    item4 = FAT32_time(new_item1)
    if file_system == 'NTFS':
        if item2 != 0: #1 la file
            messagebox.showinfo("NTFS Information", f"This volume is a NTFS system\n This is a file\n File system size: {item2} bytes\n Date created : {item3} \nTime Created: {item4}")
            return            
        item1 = calculate_folder_size(new_item1)
        messagebox.showinfo("NTFS Information", f"This volume is a NTFS system\n This is a folder\n Folder system size: {item1} bytes\n Date created : {item3} \nTime Created: {item4}")

def show_disk_info_2(file_system, item):
    new_item = treeview2.selection()[0]
    new_item1 = get_data_by_key(u1, new_item)[0][new_item]
    item2 = calculate_file_size(new_item1)
    if (get_data_by_key(u1, new_item)[0]["type"] == -1 ):
        item1 = calculate_folder_size(new_item1)
        messagebox.showinfo("FAT32 Information", f"This volume is a FAT32  system\n This is a folder\n Folder system size: {item1} bytes")
        return
    item3 = FAT32_date(new_item1)
    item4 = FAT32_time(new_item1)
    if file_system == 'FAT32':
        if item2 != 0: #1 la file
            messagebox.showinfo("FAT32 Information", f"This volume is a FAT32 system\n This is a file\n File system size: {item2} bytes \n Date created : {item3} \nTime Created: {item4}")
            return            
        item1 = calculate_folder_size(new_item1)
        messagebox.showinfo("FAT32 Information", f"This volume is a FAT32  system\n This is a folder\n Folder system size: {item1} bytes \n Date created: {item3}\n Time created: {item4}")

def read_FAT32_data(file_system, item):
    new_item = treeview2.selection()[0]
    new_item1 = get_data_by_key(u1, new_item)[0][new_item]
    item2 = fileData(new_item1)
    window = tk.Toplevel()
    # Tạo widget Text để hiển thị đoạn văn bản
    text_widget = tk.Text(window)
    text_widget.pack(fill="both", expand=True)

    # Thêm đoạn văn bản vào widget Text
    text_widget.insert("1.0", item2)

def read_NTFS_data(file_system, item):
    new_item = treeview1.selection()[0]
    new_item1 = get_data_by_key(u, new_item)[0][new_item]
    item2 = fileData(new_item1)
    window = tk.Toplevel()
    # Tạo widget Text để hiển thị đoạn văn bản
    text_widget = tk.Text(window)
    text_widget.pack(fill="both", expand=True)

    # Thêm đoạn văn bản vào widget Text
    text_widget.insert("1.0", item2)
    
def show_context_menu_1(event, item, file_system):  
    context_menu1 = tk.Menu(root, tearoff=0)
    context_menu1.add_command(label="Show Disk Information", command=lambda: show_disk_info_1(file_system, item))
    context_menu1.add_command(label="Display the inner content", command=lambda: read_NTFS_data(file_system, item))
    context_menu1.post(event.x_root, event.y_root)

def show_context_menu_2(event, item, file_system):  
    context_menu = tk.Menu(root, tearoff=0)
    context_menu.add_command(label="Show Disk Information", command=lambda: show_disk_info_2(file_system, item))
    context_menu.add_command(label="Display the inner content", command=lambda: read_FAT32_data(file_system, item))
    context_menu.post(event.x_root, event.y_root)

def FAT32_date(file_item):
    return file_item.getDate()
def FAT32_time (file_item):
    return file_item.getTime()

def NTFS_Date (file_item): 
    return file_item.getDate()

def NTFS_Time (file_item):
    return file_item.getTime()

def fileData (file_item):
    return file_item.getData()


def calculate_file_size(file_item):
    return file_item.size

def calculate_folder_size(folder_item):
    total_size = 0
    for sub_item in folder_item.son:
        if sub_item.hidden == 0 and sub_item.name != '.' and sub_item.name != '..' and sub_item.name != "":
            if sub_item.type == 1:  # Nếu là tệp tin
                total_size += sub_item.size
            elif sub_item.type == 0:  # Nếu là thư mục
                total_size += calculate_folder_size(sub_item)
    return total_size

u = []
u1 = []
def insert_treeview1(parent, item, file_system):
    if item.hidden == 0 and item.name != '.' and item.name != '..' and item.name != "":
        if item.type == 0:  # Nếu là thư mục
            folder_item = treeview1.insert(parent, tk.END, text=item.name, tags=('custom_font',), image=folder_icon)
            for sub_item in item.son:
                insert_treeview1(folder_item, sub_item, file_system)
            # Gắn sự kiện chuột phải cho thư mục
            treeview1.bind("<Button-3>", lambda event, item=item, file_system=file_system: show_context_menu_1(event, item, file_system))
            my_dict = {folder_item: item, "type" :0}
            u.append(my_dict)
        elif item.type == 1:  # Nếu là tệp tin
            small_item = treeview1.insert(parent, tk.END, text=item.name, image=file_icon)
            # Gắn sự kiện chuột phải cho tệp tin
            treeview1.bind("<Button-3>", lambda event, item=item, file_system=file_system: show_context_menu_1(event, item, file_system))
            my_dict = {small_item: item, "type": 1}
            u.append(my_dict)

def insert_treeview2(parent, item, file_system):
    if item.hidden == 0 and item.name != '.' and item.name != '..' and item.name != "":
        if item.type == 0:  # Nếu là thư mục
            folder_item = treeview2.insert(parent, tk.END, text=item.name, tags=('custom_font',), image=folder_icon)
            for sub_item in item.son:
                insert_treeview2(folder_item, sub_item, file_system)
            # Gắn sự kiện chuột phải cho thư mục
            treeview2.bind("<Button-3>", lambda event, item=item, file_system=file_system: show_context_menu_2(event, item, file_system))
            my_dict1 = {folder_item: item, "type" :0 }
            u1.append(my_dict1)
        elif item.type == 1:  # Nếu là tệp tin
            small_item1 = treeview2.insert(parent, tk.END, text=item.name, image=file_icon)
            # Gắn sự kiện chuột phải cho tệp tin
            treeview2.bind("<Button-3>", lambda event, item=item, file_system=file_system: show_context_menu_2(event, item, file_system))
            my_dict1 = {small_item1: item, "type": 1}
            u1.append(my_dict1)

mbr_usb_path = read_mbr(usb_path)
for partition in mbr_usb_path:
    if partition.type == 0: #partition = NTFS
        read_NTFS(partition)
        NTFS_name = treeview1.insert("", tk.END, text=partition.name, tags=('custom_font',), image=folder_icon)
        my_dict = {NTFS_name: partition, "type" : -1}
        u.append(my_dict)
        for sub_item in partition.son:
            folder_item = insert_treeview1(NTFS_name, sub_item, 'NTFS')
            treeview1.bind("<Button-3>", lambda event, sub_item = sub_item, file_system='NTFS': show_context_menu_1(event, sub_item, 'NTFS'))
    elif partition.type == 1:
        read_FAT32(partition) 
        FAT32_name = treeview2.insert("", tk.END, text=partition.name, tags= ('custom_font',), image=folder_icon)
        my_dict1 = {FAT32_name: partition, "type" : -1}
        u1.append(my_dict1)
        for sub_item in partition.son:
            folder_item = insert_treeview2(FAT32_name, sub_item, 'FAT32')
            treeview2.bind("<Button-3>", lambda event, sub_item=sub_item, file_system='FAT32': show_context_menu_2(event, sub_item, 'FAT32'))


print(treeview1.get_children)
print(treeview2.get_children)
treeview1.pack(expand=True, fill=tk.BOTH)
treeview2.pack(expand=True, fill=tk.BOTH)
set_window_to_fullscreen(root)

root.mainloop()



treeview1.pack(expand=True, fill=tk.BOTH)
treeview2.pack(expand=True, fill=tk.BOTH)
set_window_to_fullscreen(root)

root.mainloop()
