import os
import subprocess
import psutil
import pyautogui
import threading
import time

def close_existing_terminals():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] in ('cmd.exe', 'powershell.exe', 'bash.exe', 'python.exe'):
            try:
                proc.terminate()
                proc.wait(timeout=3)
            except psutil.NoSuchProcess:
                pass

def save_all_files():
    pyautogui.hotkey('ctrl', 'shift', 's')

def run_current_file():
    pyautogui.hotkey('ctrl', 's')
    pyautogui.hotkey('ctrl', 'shift', 'p')
    pyautogui.typewrite('Terminal: Run Active File')
    pyautogui.press('enter')

def run_main_py():
    time.sleep(1)  # Add a delay before running main.py
    subprocess.Popen(['python', 'd:/drevo/OneDrive/Documents/.Documents/repos/snipester/main.py'])

def run_main_py_in_thread():
    thread = threading.Thread(target=run_main_py)
    thread.start()

if __name__ == '__main__':
    close_existing_terminals()
    save_all_files()
    run_current_file()
    run_main_py_in_thread()
    os._exit(0)  # Close the current script's window
