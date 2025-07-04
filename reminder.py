import threading
import datetime
import time
import uuid

import dateparser
import tkinter as tk
import json
import os

from tkinter import messagebox
from core.speakers import speak

REMINDER_FILE = "config/reminder.json"

scheduled_reminders = []


def speak_and_popup(msg):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Reminder", msg)
    speak(f"Reminder: {msg}")


def schedule_reminder(msg, remind_time):
    delay = (remind_time - datetime.datetime.now()).total_seconds()

    if delay <= 0:
        return

    reminder_id = str(uuid.uuid4())

    t = threading.Timer(delay, lambda: speak_and_popup(msg))
    t.start()
    scheduled_reminders.append({
        "id": reminder_id,
        "message": msg,
        "time": remind_time,
        "thread": t
    })


def save_reminders():
    os.makedirs("config", exist_ok=True)

    with open(REMINDER_FILE, "w") as f:
        json.dump([
            {
                "id": r["id"],
                "message": r["msg"],
                "time": r["time"].isoformat()
            }
            for r in scheduled_reminders
            if r["time"] > datetime.datetime.now()            # Save only future reminders
        ], f, indent=2)


def load_reminder():
    if not os.path.exists(REMINDER_FILE):
        return

    with open(REMINDER_FILE, "r") as f:
        try:
            data = json.load(f)
            for reminder in data:
                msg = reminder["message"]
                time_obj = datetime.datetime.fromisoformat(reminder["time"])
                schedule_reminder(msg, time_obj)

        except Exception as e:
            print(f"[Error] Failed to load reminders: {e}")


def handle_reminder_cmd(query):
    query = query.lower()

    if "remind me to" in query and " at " in query:
        try:
            parts = query.split("remind me to")[1].split(" at ")
            if len(parts) == 2:
                task = parts[0].strip()
                time_str = parts[1].strip()
                remind_time = dateparser.parse(time_str)
                if not remind_time:
                    return "⏰ Sorry, I couldn't understand the time."

                schedule_reminder(task, remind_time)
                save_reminders()

                return f"✅ Reminder set: '{task}' at {remind_time.strftime('%I:%M %p')}"

        except Exception as e:
            print(f"[Error] Reminder parsing failed: {e}")
            return "⚠️ Failed to set reminder."

    elif "cancel reminder" in query:
        key = query.split("cancel reminder")[-1].strip()

        if not key:
            return "Please specify the reminder to cancel."
        removed = cancel_reminder_by_keyword(key)

        if removed:
            return f"Cancelled {len(removed)} reminder(s) matching '{key}'."
        else:
            return "🔍 No matching reminders found to cancel."

    return None


def get_upcoming_reminders():
    return [
        {"message": msg, "time": time.strftime("%Y-%m-%d %I:%M %p")}
        for msg, t in scheduled_reminders
        if t > datetime.datetime.now()
    ]


def cancel_reminder_by_keyword(key):
    removed = []

    for r in scheduled_reminders[:]:
        if key.lower() in r["message"].lower():
            r["thread"].cancel()
            scheduled_reminders.remove(r)
            removed.append(r)

    save_reminders()
    return removed
