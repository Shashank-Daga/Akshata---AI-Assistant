import getpass
import hashlib
import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config", "settings.json"))


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def load_config():
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def save_config(data):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=4)


def load_password_hash():
    config = load_config()
    return config.get("admin_password_hash")


def save_password_hash(new_hash):
    config = load_config()
    config["admin_password_hash"] = new_hash
    save_config(config)


def requires_permission(command):
    # List of sensitive commands that require permission
    restricted_commands = [
        "shutdown", "restart", "lock system", "change system password",
        "send email", "open settings"
    ]
    return any(restricted in command.lower() for restricted in restricted_commands)


def request_permission_gui():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    stored_hash = load_password_hash()
    password = simpledialog.askstring("Permission Required", "Enter admin password:", show='*')

    if password is None:
        messagebox.showinfo("Cancelled", "Permission cancelled.")
        return False

    input_hash = hash_password(password)

    if input_hash == stored_hash:
        messagebox.showinfo("Access Granted", "Permission granted.")
        return True
    else:
        messagebox.showerror("Access Denied", "Incorrect password.")
        return False


def change_password_gui():
    root = tk.Tk()
    root.withdraw()

    stored_hash = load_password_hash()

    current = simpledialog.askstring("Change Password", "Enter current password:", show='*')
    if current is None:
        return

    if hash_password(current) != stored_hash:
        messagebox.showerror("Error!", "Incorrect password.")
        return

    new_pass = simpledialog.askstring("New Password", " Enter new password:", show='*')
    confirm_pass = simpledialog.askstring("Confirm New Password", " Confirm new password", show='*')

    if new_pass != confirm_pass:
        messagebox.showerror("Error", "Password doesn't match.")
        return

    if not new_pass or len(new_pass) < 5:
        messagebox.showerror("Error", "Password is too short.")
        return

    new_hash = hash_password(new_pass)
    save_password_hash(new_hash)
    messagebox.showinfo("Success", "Password changed successfully!")
