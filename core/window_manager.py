import pygetwindow as gw
import pyautogui
import subprocess
import os
import win32gui
import win32api
import psutil


def minimize_all_windows():
    pyautogui.hotkey('win', 'd')
    return "All windows minimized."


def maximize_current_window():
    win = gw.getActiveWindow()
    if win:
        win.maximize()
        return "Current window maximized."
    return "Couldn't find the active window."


def minimize_current_window():
    win = gw.getActiveWindow()
    if win:
        win.minimize()
        return "Current window minimized."
    return "Couldn't find the active window."


def close_current_window():
    win = gw.getActiveWindow()
    if win:
        win.close()
        return "Current window closed."
    return "Couldn't find the active window."


def close_all_windows():
    closed = 0
    for win in gw.getAllWindows():
        try:
            if win.title and win.isVisible:
                win.close()
                closed += 1
        except Exception:
            continue
    return f"Closed {closed} windows."


def snap_active_window(direction):
    hwnd = win32gui.GetForegroundWindow()
    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)

    if direction == "left":
        win32gui.MoveWindow(hwnd, 0, 0, screen_width // 2, screen_height, True)
    elif direction == "right":
        win32gui.MoveWindow(hwnd, screen_width // 2, 0, screen_width // 2, screen_height, True)

    return f"Window snapped to {direction}."


def close_specific_app(app_name):
    closed = 0
    for proc in psutil.process_iter(['pid', 'name']):
        if app_name.lower() in proc.info['name'].lower():
            try:
                os.kill(proc.info['pid'], 9)
                closed += 1
            except:
                pass
    if closed > 0:
        return f"Closed {closed} {app_name} window(s)."
    else:
        return f"No running windows found for {app_name}."


def switch_window():
    pyautogui.hotkey('alt', 'tab')
    return "Switched to next window."


def open_task_manager():
    subprocess.Popen("taskmgr")
    return "Opening Task Manager."
