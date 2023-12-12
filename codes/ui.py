import tkinter as tk
from tkinter import filedialog
from surfer import Surfer
from recorder import Recorder

def browse_config():
    config_location = filedialog.askopenfilename()
    config_entry.delete(0, tk.END)
    config_entry.insert(0, config_location)

def browse_action():
    action_location = filedialog.askopenfilename()
    action_entry.delete(0, tk.END)
    action_entry.insert(0, action_location)

def start_exploratory():
    package_name = package_entry.get()
    config_location = config_entry.get()
    time_limit = time_entry.get()
    print(package_name, config_location, time_limit)
    surfer = Surfer(package_name)
    surfer.bfs(config_name=config_location, time_limit=time_limit)
    surfer.recorder.save_states()
    surfer.tree.make_html_tree()

    # Implement exploratory mode action here using the package_name, config_location, and time_limit

def start_action():
    package_name = package_entry.get()
    action_location = action_entry.get()
    time_limit = time_entry.get()
    print(package_name, action_location, time_limit)
    # Implement action mode action here using the package_name, action_location, and time_limit

root = tk.Tk()
root.title("DroidBrain")
root.geometry("400x300")  # Set initial window size

# Labels
tk.Label(root, text="Package Name").place(relx=0.3, rely=0.1, anchor="center")
tk.Label(root, text="Config File Location").place(relx=0.3, rely=0.3, anchor="center")
tk.Label(root, text="Action File Directory").place(relx=0.3, rely=0.5, anchor="center")
tk.Label(root, text="Time Limit").place(relx=0.3, rely=0.7, anchor="center")

# Entries
package_entry = tk.Entry(root)
config_entry = tk.Entry(root)
action_entry = tk.Entry(root)
time_entry = tk.Entry(root)

package_entry.place(relx=0.7, rely=0.1, anchor="center")
config_entry.place(relx=0.7, rely=0.3, anchor="center")
action_entry.place(relx=0.7, rely=0.5, anchor="center")
time_entry.place(relx=0.7, rely=0.7, anchor="center")

# Browse buttons
tk.Button(root, text="Browse", command=browse_config).place(relx=0.85, rely=0.3, anchor="center")
tk.Button(root, text="Browse", command=browse_action).place(relx=0.85, rely=0.5, anchor="center")

# Action buttons
tk.Button(root, text="Exploratory Mode", command=start_exploratory).place(relx=0.5, rely=0.85, anchor="center")
tk.Button(root, text="Action Mode", command=start_action).place(relx=0.5, rely=0.95, anchor="center")

root.mainloop()
