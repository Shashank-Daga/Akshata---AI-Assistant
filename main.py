import tkinter as tk
from threading import Thread

from tkinter import messagebox

from core.listener import get_user_input
from core.speakers import speak
from core.cmds import exe_cmd
from core.chatbot import get_chatbot_response
from core.logger import log_action, log_interaction, get_filtered_memory_logs, read_log

is_dark = True


def toggle_theme():
    global is_dark
    is_dark = not is_dark

    bg = "#ffffff" if not is_dark else "#1e1e1e"
    fg = "#000000" if not is_dark else "#00FF00"
    entry_bg = "#f0f0f0" if not is_dark else "#2e2e2e"

    window.config(bg=bg)
    input_entry.config(bg=entry_bg, fg=fg)
    output_box.config(bg=entry_bg, fg=fg)
    log_box.config(bg=entry_bg, fg=fg)
    log_label.config(bg=bg, fg=fg)
    btn_frame.config(bg=bg)


def process_input(user_input, from_voice=False):
    if not user_input:
        return

    prefix = "You (voice):" if from_voice else "You: "
    output_box.insert(tk.END, f"{prefix} {user_input}\n")
    log_action(f"User said: {user_input}")
    log_interaction("User", user_input)

    # Priority 1: Predefined commands
    result = exe_cmd(user_input)

    if result:
        speak(result)
        output_box.insert(tk.END, f"Assistant: {result}\n")
        log_action(f"Assistant: {result}")
        log_interaction("Command", result)

    else:
        # Fallback to Chatbot
        reply = get_chatbot_response(user_input)
        speak(reply)
        output_box.insert(tk.END, f"Assistant: {reply}\n")
        log_action(f"Chatbot: {reply}")
        log_interaction("Chatbot", reply)

        # Ask user to save new intent (learn)
        if "should i remember" not in user_input.lower():
            output_box.insert(tk.END, "Assistant: Should I remember this command?\n")


# Voice input thread
def handle_voice_input():
    user_input = get_user_input()
    process_input(user_input, from_voice=True)


# GUI Handlers
def on_submit():
    user_input = input_entry.get()
    input_entry.delete(0, tk.END)
    process_input(user_input)


def on_listen():
    Thread(target=handle_voice_input).start()


# View History Button Function
def open_history_window():
    history_win = tk.Toplevel(window)
    history_win.title("Interaction History")
    history_win.geometry("700x500")
    history_win.config(bg="#2b2b2b")

    tk.Label(history_win, text="Filter by:", bg="#2b2b2b", fg="white").pack()

    # Filters
    filter_frame = tk.Frame(history_win, bg="#2b2b2b")
    filter_frame.pack(pady=5)

    tk.Label(filter_frame, text="Date (YYYY-MM-DD):", bg="#2b2b2b", fg="white").grid(row=0, column=0)
    date_entry = tk.Entry(filter_frame, width=15)
    date_entry.grid(row=0, column=1, padx=5)

    tk.Label(filter_frame, text="Keyword:", bg="#2b2b2b", fg="white").grid(row=0, column=2)
    keyword_entry = tk.Entry(filter_frame, width=15)
    keyword_entry.grid(row=0, column=3, padx=5)

    tk.Label(filter_frame, text="Type:", bg="#2b2b2b", fg="white").grid(row=0, column=4)
    type_entry = tk.Entry(filter_frame, width=15)
    type_entry.grid(row=0, column=5, padx=5)

    history_display = tk.Text(history_win, width=85, height=20, bg="black", fg="lightgreen")
    history_display.pack(pady=10)

    def filter_history():
        date = date_entry.get()
        keyword = keyword_entry.get()
        log_type = type_entry.get()

        logs = get_filtered_memory_logs(date_filter=date, keyword_filter=keyword, type_filter=log_type)

        history_display.delete("1.0", tk.END)
        for log in logs:
            history_display.insert(tk.END, f"{log}\n")

    tk.Button(history_win, text="Apply Filter", command=filter_history, bg="#00bcd4", fg="white").pack()


def clear_chat():
    confirm = messagebox.askyesno("Clear Chat", "Are you sure you want to clear the chat?")
    if confirm:
        output_box.delete("1.0", tk.END)


# Log updater every 3 seconds
def update_logs():
    if log_visible:
        logs = read_log()
        log_box.config(state=tk.NORMAL)
        log_box.delete("1.0", tk.END)
        log_box.insert(tk.END, logs)
        log_box.see(tk.END)
        log_box.config(state=tk.DISABLED)
    window.after(3000, update_logs)


def toggle_logs():
    global log_visible
    log_visible = not log_visible

    if log_visible:
        log_box.pack(pady=5)
        log_label.pack()
        toggle_log_btn.config(text="🙈 Hide Logs")
    else:
        log_box.pack_forget()
        log_label.pack_forget()
        toggle_log_btn.config(text="👁️ Show Logs")


def open_tools_window():
    tools_win = tk.Toplevel(window)
    tools_win.title("Tools")
    tools_win.geometry("400x300")
    tools_win.config(bg="#2d2d2d")

    tk.Label(tools_win, text="Web Search", bg="#2d2d2d", fg="white").pack(pady=5)
    search_entry = tk.Entry(tools_win, width=40)
    search_entry.pack()
    tk.Button(tools_win, text="Search", command=lambda: process_input(f"search for {search_entry.get()}")).pack(pady=5)

    tk.Label(tools_win, text="Translate Text", bg="#2d2d2d", fg="white").pack(pady=10)
    translate_text_entry = tk.Entry(tools_win, width=40)
    translate_text_entry.pack()

    tk.Label(tools_win, text="Target Language (e.g. 'en', 'hi')", bg="#2d2d2d", fg="white").pack()
    target_lang_entry = tk.Entry(tools_win, width=10)
    target_lang_entry.pack()

    tk.Button(tools_win, text="Translate", command=lambda: process_input(f"translate {translate_text_entry.get()} to {target_lang_entry.get()}")).pack(pady=5)


def open_app_launcher():
    app_win = tk.Toplevel(window)
    app_win.title("App Launcher")
    app_win.geometry("300x200")
    app_win.config(bg="#2c2c2c")

    tk.Label(app_win, text="Select an App:", bg="#2c2c2c", fg="white").pack(pady=5)
    app_var = tk.StringVar(app_win)
    app_var.set("notepad")

    app_dropdown = tk.OptionMenu(app_win, app_var, *["notepad", "calculator", "chrome", "vscode"])
    app_dropdown.pack(pady=5)

    tk.Button(app_win, text="Launch", command=lambda: process_input(f"launch {app_var.get()}")).pack(pady=10)


# GUI Layout
window = tk.Tk()
window.title("Akshata")
window.geometry("900x800")
window.config(bg="#1e1e1e")

log_visible = True  # default state

# Input
input_entry = tk.Entry(window, width=50, font=("Arial", 14))
input_entry.pack(pady=15)

# Buttons
btn_frame = tk.Frame(window, bg="#1e1e1e")
btn_frame.pack()

submit_button = tk.Button(btn_frame, text="Send", command=on_submit, bg="#4CAF50", fg="white", width=10)
submit_button.pack(side=tk.LEFT, padx=5)

listen_button = tk.Button(btn_frame, text="🎙️ Listen", command=on_listen, bg="#2196F3", fg="white", width=10)
listen_button.pack(side=tk.LEFT, padx=5)

history_button = tk.Button(btn_frame, text="📜 View History", command=open_history_window, bg="#9c27b0", fg="white", width=15)
history_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(btn_frame, text="🧹 Clear Chat", command=clear_chat, bg="#f44336", fg="white", width=12)
clear_button.pack(side=tk.LEFT, padx=5)

toggle_log_btn = tk.Button(btn_frame, text="👁️Toggle Logs", bg="#ff9800", fg="white", width=15)
toggle_log_btn.pack(side=tk.LEFT, padx=5)
toggle_log_btn.config(command=toggle_logs)

app_btn = tk.Button(btn_frame, text="🚀 Apps", command=open_app_launcher, bg="#3f51b5", fg="white", width=10)
app_btn.pack(side=tk.LEFT, padx=5)

tools_button = tk.Button(btn_frame, text="🧰 Tools", command=open_tools_window, bg="#795548", fg="white", width=10)
tools_button.pack(side=tk.LEFT, padx=5)

theme_btn = tk.Button(btn_frame, text="🌓 Theme", command=toggle_theme, bg="#607d8b", fg="white", width=10)
theme_btn.pack(side=tk.LEFT, padx=5)

# Output Box
output_box = tk.Text(window, height=20, width=80, font=("Courier", 11), bg="#2e2e2e", fg="#00FF00")
output_box.pack(pady=10)

# Live Log Viewer Section
log_label = tk.Label(window, text="Live Log Viewer", bg="#1e1e1e", fg="#FFD700", font=("Arial", 10, "bold"))
log_label.pack()

log_box = tk.Text(window, height=12, width=100, font=("Courier", 10), bg="#121212", fg="#00FFAA")
log_box.pack(pady=5)


update_logs()
window.mainloop()
