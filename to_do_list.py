import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
from tkmacosx import Button
import json
import os
import atexit

root = Tk()
root.title("To Do List")
root.minsize(width=500, height=500)
root.config(bg="#1a1f3a" , padx=20 , pady=20)

app_data_dir = os.path.expanduser("~/.to_do_list_data")
os.makedirs(app_data_dir, exist_ok=True)
DATA_FILE = os.path.join(app_data_dir, "todo_data.json")

todos = {}
completed = {}
item_counter = 0

#-------------FUNCTİONS----------------#

def save_data():
    
    data = {
        "todos": [str(id) for id in todos.keys()],
        "completed": [str(id) for id in completed.keys()],
        "items": {}
    }
    
    for item_id in todos.keys():
        
        data["items"][str(item_id)] = todos[item_id]["text"]
    
    for item_id in completed.keys():
        
        data["items"][str(item_id)] = completed[item_id]["text"]
    
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_data():
    
    global item_counter
    
    if not os.path.exists(DATA_FILE):
        return
    
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        
        all_ids = [int(id_str) for id_str in data["items"].keys()]
        
        if all_ids:
            item_counter = max(all_ids)
        
        for item_id_str in data["todos"]:
            item_id = int(item_id_str)
            text = data["items"][str(item_id)]
            
            var = BooleanVar(value=False)
            var.trace("w", lambda name, index, mode, id=item_id: on_checkbox_toggle(id))
            
            todos[item_id] = {"text": text, "var": var}
            
            checkbox = ctk.CTkCheckBox(todo_items_frame, text=text, variable=var, 
                                  bg="#1E293B", fg="#F8FAFC", font=("Arial", 10),
                                  selectcolor="#5DADE2", activebackground="#1E293B")
            checkbox.pack(anchor="w", padx=10, pady=5)
            todos[item_id]["checkbox"] = checkbox
        
        for item_id_str in data["completed"]:
            item_id = int(item_id_str)
            text = data["items"][str(item_id)]
            
            var = BooleanVar(value=True)
            var.trace("w", lambda name, index, mode, id=item_id: on_checkbox_toggle(id))
            
            completed[item_id] = {"text": text, "var": var}
            
            checkbox = ctk.CTkCheckBox(completed_items_frame, text=text, variable=var,
                                  bg="#1E293B", fg="#F8FAFC", font=("Arial", 10),
                                  selectcolor="#5DADE2", activebackground="#1E293B")
            checkbox.pack(anchor="w", padx=10, pady=5)
            completed[item_id]["checkbox"] = checkbox
    
    except Exception as e:
        pass


def on_closing():
    
    save_data()
    root.destroy()


def adding():
    
    global item_counter
    getting_add = my_entry.get()
    
    if len(getting_add) == 0:
        messagebox.showwarning(title="Warning!", message="Please enter your to-do.")
        return
    
    item_counter += 1
    item_id = item_counter
    
    var = BooleanVar(value=False)
    var.trace("w", lambda name, index, mode, id=item_id: on_checkbox_toggle(id))
    
    todos[item_id] = {"text": getting_add, "var": var}
    
    checkbox = ctk.CTkCheckBox(todo_items_frame, text=getting_add, variable=var, 
                          bg="#1E293B", fg="#F8FAFC", font=("Arial", 10),
                          selectcolor="#5DADE2", activebackground="#1E293B")
    checkbox.pack(anchor="w", padx=10, pady=5)
    
    todos[item_id]["checkbox"] = checkbox
    
    my_entry.delete(0, END)
    save_data()


def on_checkbox_toggle(item_id):
    
    if item_id in todos:
        is_checked = todos[item_id]["var"].get()
        
        if is_checked:
            move_to_completed(item_id)
    
    elif item_id in completed:
        is_checked = completed[item_id]["var"].get()
        
        if not is_checked:
            move_to_todo(item_id)


def move_to_completed(item_id):
    
    if item_id in todos:
        
        text = todos[item_id]["text"]
        checkbox = todos[item_id]["checkbox"]
        var = todos[item_id]["var"]
        checkbox.pack_forget()
        completed[item_id] = {"text": text, "var": var}
        
        checkbox_completed = ctk.CTkCheckBox(completed_items_frame, text=text, variable=var,
                                        bg="#1E293B", fg="#F8FAFC", font=("Arial", 10),
                                        selectcolor="#5DADE2", activebackground="#1E293B")
        checkbox_completed.pack(anchor="w", padx=10, pady=5)
        completed[item_id]["checkbox"] = checkbox_completed
        
        del todos[item_id]
        save_data()


def move_to_todo(item_id):
    
    if item_id in completed:
        text = completed[item_id]["text"]
        checkbox = completed[item_id]["checkbox"]
        var = completed[item_id]["var"]
        checkbox.pack_forget()
        todos[item_id] = {"text": text, "var": var}
        
        checkbox_todo = ctk.CTkCheckBox(todo_items_frame, text=text, variable=var,
                                   bg="#1E293B", fg="#F8FAFC", font=("Arial", 10),
                                   selectcolor="#5DADE2", activebackground="#1E293B")
        checkbox_todo.pack(anchor="w", padx=10, pady=5)
        todos[item_id]["checkbox"] = checkbox_todo
        
        del completed[item_id]
        save_data()


def delete_all_todos():
    
    if len(todos) == 0:
        messagebox.showwarning(title="Warning!", message="To-Do list is empty!")
        return
    
    for item_id in list(todos.keys()):
        todos[item_id]["checkbox"].pack_forget()
    todos.clear()
    save_data()


def delete_all_completed():
    
    if len(completed) == 0:
        messagebox.showwarning(title="Warning!", message="Completed list is empty!")
        return
    
    for item_id in list(completed.keys()):
        completed[item_id]["checkbox"].pack_forget()
    completed.clear()
    save_data()


#-------------Uİ Settings----------------#

my_label = ctk.CTkLabel(root, text="TO DO LIST", font=("Arial", 24, "bold"), text_color="#FFFFFF")
my_label.grid(row=0, column=0, columnspan=2, pady=20, sticky="nsew")


entry_frame = ctk.CTkFrame(root, fg_color="transparent")
entry_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
entry_frame.grid_columnconfigure(0, weight=1)

my_entry = ctk.CTkEntry(entry_frame, placeholder_text="Add new task...", height=35)
my_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")

add_button = ctk.CTkButton(entry_frame, text="Add", font=("Arial", 12, "normal") ,fg_color="#5DADE2", width=100, height=35, command=adding)
add_button.grid(row=0, column=1)


ctk.CTkLabel(root, text="To-do's", font=("Arial", 16, "bold")).grid(row=2, column=0, pady=(10, 1))
ctk.CTkLabel(root, text="Completed", font=("Arial", 16, "bold")).grid(row=2, column=1, pady=(10, 1))


todo_items_frame = ctk.CTkScrollableFrame(root, fg_color="#1E293B", corner_radius=10)
todo_items_frame.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

completed_items_frame = ctk.CTkScrollableFrame(root, fg_color="#1E293B", corner_radius=10)
completed_items_frame.grid(row=3, column=1, padx=10, pady=5, sticky="nsew")


delete_button1 = ctk.CTkButton(root, text="Clear List", fg_color="#E74C3C", hover_color="#C0392B", command=delete_all_todos)
delete_button1.configure(width=50, height=30)
delete_button1.grid(row=4, column=0, padx=10, pady=20, sticky="ew")


delete_button2 = ctk.CTkButton(root, text="Clear Completed", fg_color="#E74C3C", hover_color="#C0392B", command=delete_all_completed)
delete_button2.configure(width=50, height=30)
delete_button2.grid(row=4, column=1, padx=10, pady=20, sticky="ew")


load_data()
atexit.register(save_data)
root.protocol("WM_DELETE_WINDOW", lambda: [save_data(), root.destroy()])

root.mainloop()

