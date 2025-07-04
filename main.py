import tkinter as tk
from threading import Thread

from core.listener import get_user_input
from core.speakers import speak
from core.cmds import exe_cmd
from core.chatbot import get_chatbot_response
from core.logger import log_action, log_interaction, get_filtered_memory_logs


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


# GUI Layout
window = tk.Tk()
window.title("Akshata")
window.geometry("700x500")
window.config(bg="#1e1e1e")

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


# Output
output_box = tk.Text(window, height=20, width=80, font=("Courier", 11), bg="#2e2e2e", fg="#00FF00")
output_box.pack(pady=10)

window.mainloop()
